"""
Canonical Domain Event Catalog and Envelope (EC-EVT-002, ADR-009).

Defines `EventEnvelope`, correlation tracing (`FR-012`), and base schemas for all Level 7 domain events.
"""
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field


class EventEnvelope(BaseModel):
    """EC-EVT-002: Canonical event envelope wrapping all domain events."""
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str
    occurred_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    correlation_id: str = Field(..., description="Traces a full evolution cycle across bounded contexts")
    causation_id: Optional[str] = Field(default=None, description="ID of the event or command that caused this event")
    producer: str = Field(..., description="ID of the engine/service that produced this event")
    schema_version: str = Field(default="0.1.0")
    payload: Dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EventEnvelope":
        return cls(**data)


class DomainEvent(BaseModel):
    """Base class for specific typed domain events."""
    event_type: str = "DomainEvent"
    schema_version: str = "0.1.0"

    def wrap(self, producer: str, correlation_id: str, causation_id: Optional[str] = None) -> EventEnvelope:
        return EventEnvelope(
            event_type=self.event_type,
            correlation_id=correlation_id,
            causation_id=causation_id,
            producer=producer,
            schema_version=self.schema_version,
            payload=self.model_dump()
        )


# Canonical Core Domain Events (Volume 2 Section 9.2 & Level 7 Ontology)

class ObservationIntegrated(DomainEvent):
    """Emitted when ObservationGateway validates and integrates an observation."""
    event_type: str = "ObservationIntegrated"
    observation_id: str
    feedback_level: int  # 1 to 5
    scope: Dict[str, str]
    metrics: Dict[str, float]


class LessonExtracted(DomainEvent):
    """Emitted when LearningEngine extracts a statistically valid lesson."""
    event_type: str = "LessonExtracted"
    lesson_id: str
    knowledge_record_id: str
    rule_statement: str
    confidence: float
    p_value: Optional[float] = None


class KnowledgeActivated(DomainEvent):
    """Emitted when KnowledgeRecord transitions from CANDIDATE to ACTIVE."""
    event_type: str = "KnowledgeActivated"
    knowledge_record_id: str
    scope: Dict[str, str]
    confidence: float


class BeliefRevised(DomainEvent):
    """Emitted when BeliefEngine updates confidence based on evidence."""
    event_type: str = "BeliefRevised"
    belief_id: str
    old_confidence: float
    new_confidence: float
    evidence_id: str


class BeliefUpdated(DomainEvent):
    """Emitted when BeliefEngine updates confidence based on evidence (`FR-EC-202`)."""
    event_type: str = "BeliefUpdated"
    belief_id: str
    old_confidence: float
    new_confidence: float
    reason: str


class HypothesisGenerated(DomainEvent):
    """Emitted when HypothesisEngine generates a falsifiable testable candidate."""
    event_type: str = "HypothesisGenerated"
    hypothesis_id: str
    statement: str
    target_metric: str
    expected_direction: str


class DecisionRecorded(DomainEvent):
    """Emitted when DecisionEngine records an 8-step decision choice."""
    event_type: str = "DecisionRecorded"
    decision_id: str
    selected_candidate_id: str
    rejected_candidate_ids: list[str]
    rationale: str
    confidence: float


class DecisionMade(DomainEvent):
    """Emitted when DecisionEngine records an 8-step decision choice (`FR-EC-210`)."""
    event_type: str = "DecisionMade"
    decision_id: str
    decision_type: str
    selected_option: str
    policy_used: str


class StrategyUpdated(DomainEvent):
    """Emitted when StrategyEngine updates state (`FR-EC-220/221`)."""
    event_type: str = "StrategyUpdated"
    strategy_id: str
    new_status: str
    reason: str


class ExperimentDirectiveIssued(DomainEvent):
    """Emitted when ExperimentEngine issues a directive to Execution layer."""
    event_type: str = "ExperimentDirectiveIssued"
    experiment_id: str
    genome_version: str
    target_scope: Dict[str, str]
    parameters: Dict[str, Any]


class EvolutionCycleStarted(DomainEvent):
    """Emitted by EvolutionCycleSaga when starting a cycle."""
    event_type: str = "EvolutionCycleStarted"
    cycle_id: str
    seed: Optional[int] = None


class EvolutionCycleCompleted(DomainEvent):
    """Emitted when an evolution cycle saga reaches terminal completion."""
    event_type: str = "EvolutionCycleCompleted"
    cycle_id: str
    summary: Dict[str, Any]
