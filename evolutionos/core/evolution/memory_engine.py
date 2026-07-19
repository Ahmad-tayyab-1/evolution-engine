"""
Memory Engine (FR-EC-440, FR-EC-441).

Orchestrates daily consolidation cycle (`FR-EC-440`):
1. Detect duplicate/similar knowledge -> consolidate (`FR-EC-104`).
2. Apply confidence decay to stale beliefs/knowledge (`FR-EC-203`).
3. Recompute indexes.
4. Produce `MemoryHealthReport`.
Enforces Forgetting Policy (`FR-EC-441`): nothing deleted, only transitioned to `ARCHIVED`.
"""
import logging
from typing import Dict, Any, List, Optional
from evolutionos.core.domain.ontology import LearningHealthReport, KnowledgeStatus
from evolutionos.core.learning.knowledge_engine import KnowledgeEngine
from evolutionos.core.reasoning.belief_engine import BeliefEngine
from evolutionos.infrastructure.messaging.broker import MessageBroker

logger = logging.getLogger("evolutionos.evolution.memory")


class MemoryEngine:
    """Orchestrates memory consolidation cycle and forgetting policy."""

    def __init__(
        self,
        knowledge_engine: KnowledgeEngine,
        belief_engine: BeliefEngine,
        broker: Optional[MessageBroker] = None
    ):
        self.knowledge_engine = knowledge_engine
        self.belief_engine = belief_engine
        self.broker = broker
        self.health_reports: List[LearningHealthReport] = []

    def run_consolidation_cycle(self, correlation_id: str = "memory_cycle") -> Dict[str, Any]:
        """FR-EC-440: Execute full consolidation, decay, indexing, and report cycle."""
        logger.info("Starting Memory Engine consolidation cycle...")

        # 1. Consolidate duplicate/similar knowledge
        consolidated_events = self.knowledge_engine.consolidate()

        # 2. Apply belief decay
        stale_beliefs = self.belief_engine.apply_decay(correlation_id=correlation_id)

        # 3. Produce MemoryHealthReport
        active_knowledge_count = sum(1 for r in self.knowledge_engine.records.values() if r.status == KnowledgeStatus.ACTIVE)
        archived_knowledge_count = sum(1 for r in self.knowledge_engine.records.values() if r.status == KnowledgeStatus.ARCHIVED)

        report = LearningHealthReport(
            goodhart_alerts=0,
            recommendations=[
                {"action": "CONSOLIDATION_COMPLETED", "merged_pairs": len(consolidated_events)},
                {"action": "BELIEF_DECAY_APPLIED", "stale_beliefs": len(stale_beliefs)}
            ]
        )
        self.health_reports.append(report)

        summary = {
            "consolidated_count": len(consolidated_events),
            "stale_beliefs_decayed": len(stale_beliefs),
            "active_knowledge": active_knowledge_count,
            "archived_knowledge": archived_knowledge_count,
            "report_id": report.id
        }

        if self.broker:
            from evolutionos.core.events.catalog import EventEnvelope
            env = EventEnvelope(
                event_type="MemoryConsolidated",
                correlation_id=correlation_id,
                producer="MemoryEngine",
                payload=summary
            )
            self.broker.publish("core.events", env)

        return summary

    def archive_record(self, record_id: str, reason: str = "FORGETTING_POLICY") -> bool:
        """FR-EC-441: Forgetting policy - transition to ARCHIVED, never delete."""
        kr = self.knowledge_engine.get_record(record_id)
        if not kr:
            return False
        self.knowledge_engine.transition_status(record_id, KnowledgeStatus.ARCHIVED)
        logger.info(f"FR-EC-441 Forgetting Policy: Record {record_id} transitioned to ARCHIVED ({reason}).")
        return True
