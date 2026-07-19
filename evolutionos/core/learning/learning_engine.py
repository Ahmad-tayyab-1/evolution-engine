"""
Learning Engine (FR-EC-110, FR-EC-111, FR-EC-112).

Extracts directional lessons from completed experiment reflections, checks statistical guardrails
for promotion (`min_evidence_count = 3`), handles contradictions, and emits `LessonExtracted`.
"""
import logging
from typing import Any, Dict, List, Optional
from evolutionos.core.domain.ontology import (
    ReflectionReport, Lesson, KnowledgeRecord, KnowledgeType, KnowledgeStatus, Provenance
)
from evolutionos.core.learning.knowledge_engine import KnowledgeEngine
from evolutionos.core.events.catalog import LessonExtracted, EventEnvelope
from evolutionos.infrastructure.messaging.broker import MessageBroker
from evolutionos.config.settings import settings

logger = logging.getLogger("evolutionos.learning")


class LearningEngine:
    """Extracts lessons from reflections, enforces guardrails, and manages promotions/contradictions."""

    def __init__(self, knowledge_engine: KnowledgeEngine, broker: Optional[MessageBroker] = None):
        self.knowledge_engine = knowledge_engine
        self.broker = broker
        self.lessons: Dict[str, Lesson] = {}

    def extract_lessons(self, reflection: ReflectionReport, correlation_id: str) -> List[Lesson]:
        """FR-EC-110: Extract candidate lessons from reflection delta and attribution."""
        extracted = []
        exp_id = reflection.experiment_id

        # Look at per-metric deltas
        for metric_name, delta_info in reflection.delta.get("per_metric", {}).items():
            if not isinstance(delta_info, dict):
                continue
            pred = delta_info.get("predicted", 0.0)
            actual = delta_info.get("actual", 0.0)
            rel_delta = delta_info.get("relative_delta", 0.0)

            if abs(rel_delta) >= 0.05:  # Noticeable effect
                direction = "POSITIVE" if actual >= pred else "NEGATIVE"
                claim = f"Mutation on {metric_name} resulted in {direction.lower()} shift of {rel_delta:.1%} (actual={actual}, pred={pred})"

                # Create KnowledgeRecord (CANDIDATE status per FR-EC-111)
                kr = KnowledgeRecord(
                    type=KnowledgeType.LESSON,
                    statement=claim,
                    confidence=0.60 if abs(rel_delta) >= 0.15 else 0.40,
                    evidence_refs=[exp_id],
                    provenance=Provenance(source_type="REFLECTION", source_id=reflection.id, created_by_engine="LearningEngine"),
                    status=KnowledgeStatus.CANDIDATE
                )
                kr_id = self.knowledge_engine.add_record(kr)

                lesson = Lesson(
                    knowledge_record_id=kr_id,
                    experiment_id=exp_id,
                    direction=direction,
                    dimension=metric_name,
                    claim=claim,
                    supporting_observations=reflection.actual.get("observation_refs", []),
                    confidence_at_creation=kr.confidence
                )
                self.lessons[kr_id] = lesson
                extracted.append(lesson)

                # Emit LessonExtracted event
                event = LessonExtracted(
                    lesson_id=kr_id,
                    knowledge_record_id=kr_id,
                    rule_statement=claim,
                    confidence=kr.confidence
                )
                if self.broker:
                    env = event.wrap(producer="LearningEngine", correlation_id=correlation_id)
                    self.broker.publish("core.events", env)

        return extracted

    def evaluate_promotion(self, knowledge_record_id: str) -> bool:
        """FR-EC-111: Check statistical guardrails for promoting CANDIDATE to ACTIVE."""
        kr = self.knowledge_engine.get_record(knowledge_record_id)
        if not kr or kr.status != KnowledgeStatus.CANDIDATE:
            return False

        # Check guardrail 1: Supporting experiments >= min_evidence_count
        if len(kr.evidence_refs) < settings.min_evidence_count:
            return False

        # Check guardrail 2: No active contradiction with higher confidence
        for contra_id in kr.contradiction_refs:
            contra = self.knowledge_engine.get_record(contra_id)
            if contra and contra.status == KnowledgeStatus.ACTIVE and contra.confidence > kr.confidence:
                return False

        # Promote to ACTIVE!
        self.knowledge_engine.transition_status(kr.id, KnowledgeStatus.ACTIVE)
        return True

    def handle_contradiction(self, knowledge_record_id: str, contradictory_evidence_id: str, correlation_id: str) -> None:
        """FR-EC-112: Handle contradiction by lowering confidence and deprecating if below threshold."""
        kr = self.knowledge_engine.get_record(knowledge_record_id)
        if not kr:
            return

        kr.contradiction_refs.append(contradictory_evidence_id)
        # Apply confidence discount
        kr.confidence = max(0.01, kr.confidence * 0.70)

        if kr.confidence < settings.deprecation_threshold and kr.status in [KnowledgeStatus.ACTIVE, KnowledgeStatus.CANDIDATE]:
            logger.warning(f"KnowledgeRecord {kr.id} dropped below deprecation threshold ({kr.confidence:.2f}). Transitioning to DEPRECATED.")
            self.knowledge_engine.transition_status(kr.id, KnowledgeStatus.DEPRECATED)

            # Emit BeliefRevisionRequired event
            if self.broker:
                env = EventEnvelope(
                    event_type="BeliefRevisionRequired",
                    correlation_id=correlation_id,
                    producer="LearningEngine",
                    payload={"knowledge_record_id": kr.id, "new_confidence": kr.confidence, "reason": "CONTRADICTION"}
                )
                self.broker.publish("engine.belief", env)
