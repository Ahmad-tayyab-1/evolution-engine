"""
Level 0-6 Canonical Domain Ontology (Volume 6 §3-7, ONT-001).

Defines immutable data structures and validation contracts across Perception, Knowledge,
Cognition, Action, Governance, and Relation levels.
"""
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, model_validator


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id() -> str:
    return str(uuid.uuid4())


# ==========================================
# Level 0 — Base Types & Scope
# ==========================================

class VariableType(str, Enum):
    CONTINUOUS = "CONTINUOUS"
    ORDINAL = "ORDINAL"
    CATEGORICAL = "CATEGORICAL"
    BINARY = "BINARY"


class Scope(BaseModel):
    """Level 0 Scope: Contextual boundary within which knowledge/beliefs apply."""
    niche: Optional[str] = None
    platform: Optional[str] = None
    audience_segment: Optional[str] = None
    format: Optional[str] = None
    language: Optional[str] = None
    region: Optional[str] = None

    def specificity_score(self) -> int:
        """Count of non-null fields."""
        return sum(1 for v in self.model_dump().values() if v is not None)

    def is_compatible_with(self, other: "Scope") -> bool:
        """Two scopes are compatible if every non-null field matches."""
        d_self = self.model_dump()
        d_other = other.model_dump()
        for k in d_self:
            v1, v2 = d_self[k], d_other[k]
            if v1 is not None and v2 is not None and v1 != v2:
                return False
        return True


class Variable(BaseModel):
    """Level 0 Variable: Smallest unit of experimental interest."""
    id: str = Field(default_factory=new_id)
    name: str
    label: str
    type: VariableType
    domain: Dict[str, Any] = Field(default_factory=dict)
    unit: Optional[str] = None
    scope_applicability: List[Scope] = Field(default_factory=list)
    is_manipulable: bool = True
    is_observable: bool = True

    @model_validator(mode="after")
    def check_usefulness(self) -> "Variable":
        if not self.is_manipulable and not self.is_observable:
            raise ValueError("Variable invariant: must be either manipulable or observable.")
        return self


class AggregationType(str, Enum):
    SUM = "SUM"
    AVG = "AVG"
    RATE = "RATE"
    RATIO = "RATIO"
    PERCENTILE = "PERCENTILE"


class Metric(BaseModel):
    """Level 0 Metric: Measured expression of a Variable within context."""
    id: str = Field(default_factory=new_id)
    canonical_name: str
    variable_ref: str
    aggregation: AggregationType
    collection_window: str = "24h"
    platform_mappings: Dict[str, str] = Field(default_factory=dict)
    quality_floor: float = 0.5


# ==========================================
# Level 1 — Perception
# ==========================================

class ObservationQualityReliability(str, Enum):
    CONFIRMED = "CONFIRMED"
    ESTIMATED = "ESTIMATED"
    DISPUTED = "DISPUTED"


class ObservationQualityFreshness(str, Enum):
    CURRENT = "CURRENT"
    DELAYED = "DELAYED"
    STALE = "STALE"


class ObservationQuality(BaseModel):
    completeness: float = Field(ge=0.0, le=1.0, default=1.0)
    reliability: ObservationQualityReliability = ObservationQualityReliability.CONFIRMED
    freshness: ObservationQualityFreshness = ObservationQualityFreshness.CURRENT


class ObservationStatus(str, Enum):
    RECEIVED = "RECEIVED"
    VALIDATED = "VALIDATED"
    QUARANTINED = "QUARANTINED"
    INTEGRATED = "INTEGRATED"


class Observation(BaseModel):
    """Level 1 Observation: Single, timestamped measurement."""
    id: str = Field(default_factory=new_id)
    experiment_id: str
    platform: str
    metric: str
    value: Union[float, int, Dict[str, Any]]
    unit: str = ""
    measured_at: str = Field(default_factory=utc_now)
    collection_window: str = "24h"
    collection_method: str = "AUTOMATED"
    quality: ObservationQuality = Field(default_factory=ObservationQuality)
    raw_source_ref: Optional[str] = None
    status: ObservationStatus = ObservationStatus.RECEIVED
    supersedes_id: Optional[str] = None


class FeedbackSignal(BaseModel):
    """Level 1 FeedbackSignal: Classified observation assigned to Level 1-5."""
    id: str = Field(default_factory=new_id)
    observation_refs: List[str] = Field(default_factory=list)
    feedback_level: int = Field(ge=1, le=5)
    routing_targets: List[str] = Field(default_factory=list)
    summary: str
    detected_at: str = Field(default_factory=utc_now)


# ==========================================
# Level 2 — Knowledge
# ==========================================

class KnowledgeType(str, Enum):
    FACT = "FACT"
    PATTERN = "PATTERN"
    RULE = "RULE"
    LESSON = "LESSON"
    EXTERNAL_CLAIM = "EXTERNAL_CLAIM"


class KnowledgeStatus(str, Enum):
    CANDIDATE = "CANDIDATE"
    ACTIVE = "ACTIVE"
    DEPRECATED = "DEPRECATED"
    ARCHIVED = "ARCHIVED"


class Provenance(BaseModel):
    source_type: str = "EXPERIMENT"
    source_id: str
    created_by_engine: str
    created_at: str = Field(default_factory=utc_now)


class KnowledgeRecord(BaseModel):
    """Level 2 KnowledgeRecord: Atomic persistent unit of learning."""
    id: str = Field(default_factory=new_id)
    type: KnowledgeType
    subtype: str = ""
    statement: str
    formal_statement: Optional[Dict[str, Any]] = None
    scope: Scope = Field(default_factory=Scope)
    confidence: float = Field(ge=0.01, le=0.99)
    confidence_basis: str = "COMPUTED"
    evidence_refs: List[str] = Field(default_factory=list)
    contradiction_refs: List[str] = Field(default_factory=list)
    provenance: Provenance
    status: KnowledgeStatus = KnowledgeStatus.CANDIDATE
    validation_count: int = 0
    last_validated_at: str = Field(default_factory=utc_now)
    embedding_vector: List[float] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    supersedes_id: Optional[str] = None
    superseded_by_id: Optional[str] = None


class Rule(BaseModel):
    """Level 2 Rule: Conditional IF-THEN structure."""
    knowledge_record_id: str
    condition: Dict[str, Any]
    outcome: Dict[str, Any]
    scope: Scope
    confidence: float = Field(ge=0.01, le=0.99)
    support_count: int = 1
    contradiction_count: int = 0
    effect_size: float = 0.0
    p_value_equivalent: Optional[float] = None


class Lesson(BaseModel):
    """Level 2 Lesson: Directional learning claim from Reflection."""
    knowledge_record_id: str
    experiment_id: str
    direction: str = "POSITIVE"
    dimension: str
    claim: str
    supporting_observations: List[str] = Field(default_factory=list)
    confidence_at_creation: float = Field(ge=0.01, le=0.99)
    promoted_to_rule: bool = False
    promotion_rule_id: Optional[str] = None


class KnowledgeRelation(str, Enum):
    EVIDENCE_FOR = "EVIDENCE_FOR"
    CONTRADICTS = "CONTRADICTS"
    DERIVED_FROM = "DERIVED_FROM"
    SUPERSEDES = "SUPERSEDES"
    CONSOLIDATED_INTO = "CONSOLIDATED_INTO"
    TRANSFERRED_FROM = "TRANSFERRED_FROM"
    RELATES_TO = "RELATES_TO"
    SPECIALIZES = "SPECIALIZES"


class KnowledgeEdge(BaseModel):
    """Level 2/6 KnowledgeEdge: Typed relationship between records."""
    id: str = Field(default_factory=new_id)
    from_id: str
    to_id: str
    relation: KnowledgeRelation
    weight: float = Field(ge=0.0, le=1.0, default=1.0)
    created_at: str = Field(default_factory=utc_now)
    provenance: Provenance


# ==========================================
# Level 3 — Cognition
# ==========================================

class ConfidencePoint(BaseModel):
    timestamp: str = Field(default_factory=utc_now)
    confidence: float = Field(ge=0.01, le=0.99)
    trigger: str
    causing_event_id: str


class BeliefStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    RETIRED = "RETIRED"


class Belief(BaseModel):
    """Level 3 Belief: Confidence-weighted conclusion derived from knowledge."""
    id: str = Field(default_factory=new_id)
    statement: str
    scope: Scope = Field(default_factory=Scope)
    confidence: float = Field(ge=0.01, le=0.99)
    stability_score: float = Field(ge=0.0, le=1.0, default=1.0)
    is_load_bearing: bool = False
    derived_from: List[str] = Field(default_factory=list)
    confidence_history: List[ConfidencePoint] = Field(default_factory=list)
    last_challenged_at: Optional[str] = None
    last_validated_at: Optional[str] = None
    status: BeliefStatus = BeliefStatus.ACTIVE


class FalsifiableForm(BaseModel):
    if_variable: str
    changes_from: Any
    changes_to: Any
    in_scope: Scope
    then_metric: str
    change_direction: str
    change_magnitude: Dict[str, float] = Field(default_factory=lambda: {"min": 0.05, "max": 0.50})
    within_window: str = "72h"
    expected_confidence: float = Field(ge=0.01, le=0.99, default=0.75)


class HypothesisStatus(str, Enum):
    PROPOSED = "PROPOSED"
    ACTIVE = "ACTIVE"
    CONFIRMED = "CONFIRMED"
    FALSIFIED = "FALSIFIED"
    ABANDONED = "ABANDONED"


class Hypothesis(BaseModel):
    """Level 3 Hypothesis: Falsifiable prediction."""
    id: str = Field(default_factory=new_id)
    experiment_id: Optional[str] = None
    formal_form: FalsifiableForm
    source: Dict[str, Any] = Field(default_factory=dict)
    priority_score: float = 0.5
    status: HypothesisStatus = HypothesisStatus.PROPOSED


class MetricPrediction(BaseModel):
    metric: str
    expected_value: float
    expected_range: Dict[str, float]
    measurement_window: str = "24h"


class Prediction(BaseModel):
    """Level 3 Prediction: Forecast attached to an Experiment."""
    id: str = Field(default_factory=new_id)
    experiment_id: str
    hypothesis_id: str
    metric_predictions: List[MetricPrediction] = Field(default_factory=list)
    stated_at: str = Field(default_factory=utc_now)
    stated_confidence: float = Field(ge=0.01, le=0.99, default=0.75)
    knowledge_used: List[str] = Field(default_factory=list)
    beliefs_used: List[str] = Field(default_factory=list)


class Candidate(BaseModel):
    id: str = Field(default_factory=new_id)
    type: str
    value: Any
    score: float
    score_breakdown: Dict[str, float] = Field(default_factory=dict)
    risk: float = 0.0
    novelty: float = 0.0


class Decision(BaseModel):
    """Level 3 Decision: Irrevocable 8-step choice record."""
    id: str = Field(default_factory=new_id)
    type: str
    context: Dict[str, Any] = Field(default_factory=dict)
    candidates: List[Candidate] = Field(default_factory=list)
    scores: List[Dict[str, Any]] = Field(default_factory=list)
    knowledge_used: List[str] = Field(default_factory=list)
    beliefs_used: List[str] = Field(default_factory=list)
    policy: str = "EXPLOIT"
    selected_candidate_id: str
    rejection_reasons: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    risk_score: float = 0.0
    prediction: Optional[Prediction] = None
    made_at: str = Field(default_factory=utc_now)
    made_by: str = "DecisionEngine"


class StrategyStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    UNDER_REVIEW = "UNDER_REVIEW"
    RETIRED = "RETIRED"


class Strategy(BaseModel):
    """Level 3 Strategy: Multi-experiment plan pursuing strategic objective."""
    id: str = Field(default_factory=new_id)
    objective: Dict[str, Any]
    horizon_count: int = 5
    active_experiments: List[str] = Field(default_factory=list)
    hypothesis_backlog: List[str] = Field(default_factory=list)
    fitness_trend: List[Dict[str, Any]] = Field(default_factory=list)
    weight_profile_id: str = "default_weights"
    expiration: Dict[str, Any] = Field(default_factory=lambda: {"type": "EXPERIMENT_COUNT", "value": 10})
    review_triggers: List[Dict[str, Any]] = Field(default_factory=list)
    status: StrategyStatus = StrategyStatus.DRAFT


# ==========================================
# Level 4 — Action
# ==========================================

class Mutation(BaseModel):
    """Level 4 Mutation: Single intentional change (`FR-EC-420`, `ADR-019`)."""
    id: str = Field(default_factory=new_id)
    experiment_id: str
    mutation_class: str = Field("TOPIC", alias="class")
    variable_id: str
    baseline_value: Any
    mutated_value: Any
    distance: str = "NEAR"
    justification: str
    evaluation_mode: str = "LIVE"  # "LIVE" or "SHADOW" (ADR-019 for META/STRATEGIC mutations)

    class Config:
        populate_by_name = True


class ExperimentState(str, Enum):
    DRAFT = "DRAFT"
    HYPOTHESIZED = "HYPOTHESIZED"
    APPROVED = "APPROVED"
    SCHEDULED = "SCHEDULED"
    EXECUTING = "EXECUTING"
    MEASURING = "MEASURING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REFLECTED = "REFLECTED"
    ARCHIVED = "ARCHIVED"


class ExperimentClass(str, Enum):
    VALIDATION = "VALIDATION"
    INCREMENTAL = "INCREMENTAL"
    EXPLORATORY = "EXPLORATORY"
    RADICAL = "RADICAL"
    META = "META"


class ExperimentDirective(BaseModel):
    """Level 4 ExperimentDirective: Instruction package to execution layer."""
    id: str = Field(default_factory=new_id)
    experiment_id: str
    issued_at: str = Field(default_factory=utc_now)
    content_spec: Dict[str, Any] = Field(default_factory=dict)
    publishing_spec: Dict[str, Any] = Field(default_factory=dict)
    measurement_plan: Dict[str, Any] = Field(default_factory=dict)
    constraints: Dict[str, Any] = Field(default_factory=dict)


class Experiment(BaseModel):
    """Level 4 Experiment: Controlled attempt to validate hypothesis."""
    id: str = Field(default_factory=new_id)
    strategy_id: str
    hypothesis_id: str
    baseline_ref: Optional[str] = None
    mutations: List[Mutation] = Field(default_factory=list)
    directive: Optional[ExperimentDirective] = None
    prediction: Optional[Prediction] = None
    measurement_plan: Dict[str, Any] = Field(default_factory=dict)
    risk_score: float = 0.0
    experiment_class: ExperimentClass = Field(ExperimentClass.INCREMENTAL, alias="class")
    state: ExperimentState = ExperimentState.DRAFT
    timeline: List[Dict[str, Any]] = Field(default_factory=list)

    class Config:
        populate_by_name = True


class ReflectionReport(BaseModel):
    """Level 4 ReflectionReport: Mandatory output of terminal experiment."""
    id: str = Field(default_factory=new_id)
    experiment_id: str
    prediction: Dict[str, Any] = Field(default_factory=dict)
    actual: Dict[str, Any] = Field(default_factory=dict)
    delta: Dict[str, Any] = Field(default_factory=dict)
    surprise_score: float = Field(ge=0.0, le=1.0, default=0.0)
    attribution: List[Dict[str, Any]] = Field(default_factory=list)
    confounds_identified: List[str] = Field(default_factory=list)
    lessons_proposed: List[str] = Field(default_factory=list)
    calibration_impact: Dict[str, Any] = Field(default_factory=dict)
    meta_notes: str = ""
    generated_at: str = Field(default_factory=utc_now)
    validated: bool = False


class FitnessVector(BaseModel):
    learning_yield: float = 0.0
    prediction_accuracy: float = 0.0
    performance_delta: float = 0.0
    strategic_alignment: float = 0.0
    cost_efficiency: float = 0.0


class FitnessRecord(BaseModel):
    """Level 4 FitnessRecord: Multi-objective evaluation."""
    id: str = Field(default_factory=new_id)
    experiment_id: str
    weight_profile_id: str = "default_weights"
    vector: FitnessVector = Field(default_factory=FitnessVector)
    scalar: float = 0.0
    computed_at: str = Field(default_factory=utc_now)


class CycleStep(str, Enum):
    MEMORY_CONSOLIDATION = "MEMORY_CONSOLIDATION"
    BELIEF_DECAY = "BELIEF_DECAY"
    HYPOTHESIS_REFRESH = "HYPOTHESIZED"
    STRATEGY_REVIEW = "STRATEGY_REVIEW"
    EXPERIMENT_SELECTION = "EXPERIMENT_SELECTION"
    DIRECTIVE_ISSUANCE = "DIRECTIVE_ISSUANCE"
    AWAITING_EXECUTION = "AWAITING_EXECUTION"
    OBSERVATION_INGESTION = "OBSERVATION_INGESTION"
    REFLECTION = "REFLECTION"
    LESSON_EXTRACTION = "LESSON_EXTRACTION"
    FITNESS_COMPUTATION = "FITNESS_COMPUTATION"
    META_EVALUATION = "META_EVALUATION"
    COMPLETED = "COMPLETED"


class EvolutionCycle(BaseModel):
    """Level 4 EvolutionCycle: Complete iteration of evolution saga."""
    id: str = Field(default_factory=new_id)
    sequence: int
    started_at: str = Field(default_factory=utc_now)
    completed_at: Optional[str] = None
    step: CycleStep = CycleStep.MEMORY_CONSOLIDATION
    experiments_issued: List[str] = Field(default_factory=list)
    experiments_completed: List[str] = Field(default_factory=list)
    lessons_extracted: int = 0
    beliefs_revised: int = 0
    knowledge_created: int = 0
    cycle_fitness: float = 0.0
    status: str = "RUNNING"


# ==========================================
# Level 5 — Governance
# ==========================================

class GovernancePolicy(BaseModel):
    id: str = Field(default_factory=new_id)
    version: str = "0.1.0"
    effective_from: str = Field(default_factory=utc_now)
    parameters: Dict[str, Any] = Field(default_factory=dict)


class AuditEvent(BaseModel):
    id: str = Field(default_factory=new_id)
    timestamp: str = Field(default_factory=utc_now)
    actor: str
    action: str
    target_entity: str
    context: str
    outcome: str = "SUCCESS"
    is_override: bool = False


class LearningHealthReport(BaseModel):
    id: str = Field(default_factory=new_id)
    cycle_window: List[int] = Field(default_factory=lambda: [1, 10])
    generated_at: str = Field(default_factory=utc_now)
    prediction_error_trend: str = "STABLE"
    calibration_error: float = 0.05
    learning_yield: float = 1.2
    exploration_effectiveness: float = 0.8
    cost_per_validated_lesson: float = 0.15
    belief_stability_avg: float = 0.92
    goodhart_alerts: int = 0
    recommendations: List[Dict[str, Any]] = Field(default_factory=list)
