"""
Unit tests for Phase 1 Perception and Learning Engines (`FR-EC-101` through `FR-EC-122`).
"""
import pytest
from evolutionos.core.domain.ontology import (
    Observation, ObservationStatus, KnowledgeRecord, KnowledgeType, KnowledgeStatus, Provenance,
    Scope, Experiment, Prediction, MetricPrediction, Mutation
)
from evolutionos.core.perception.observation_gateway import ObservationGateway
from evolutionos.core.perception.signal_classifier import SignalClassifier
from evolutionos.core.learning.knowledge_engine import KnowledgeEngine
from evolutionos.core.learning.learning_engine import LearningEngine
from evolutionos.core.learning.reflection_engine import ReflectionEngine
from evolutionos.infrastructure.messaging.redis_streams import MemoryBroker


def test_observation_gateway_quarantine_and_integration():
    """Verify ObservationGateway quarantines impossible values and integrates valid observations."""
    broker = MemoryBroker()
    gateway = ObservationGateway(broker=broker)

    # 1. Impossible CTR percentage (>100%)
    raw_impossible = {
        "experiment_id": "exp_01",
        "platform": "youtube",
        "metric": "ctr",
        "value": 150.0,
        "unit": "%"
    }
    obs, reason = gateway.process_observation(raw_impossible, correlation_id="corr_1")
    assert obs.status == ObservationStatus.QUARANTINED
    assert "Impossible percentage value" in reason
    assert len(gateway.quarantine_log) == 1

    # 2. Valid observation
    raw_valid = {
        "experiment_id": "exp_01",
        "platform": "youtube",
        "metric": "selection_rate",
        "value": 0.085,
        "unit": "ratio"
    }
    obs_valid, reason_valid = gateway.process_observation(raw_valid, correlation_id="corr_2")
    assert obs_valid.status == ObservationStatus.INTEGRATED
    assert reason_valid is None
    assert len(gateway.integrated_log) == 1


def test_signal_classifier_routing():
    """Verify SignalClassifier assigns levels 1-5 correctly."""
    classifier = SignalClassifier()
    obs_error = Observation(experiment_id="exp_x", platform="youtube", metric="api_error_rate", value=0.01)
    obs_ctr = Observation(experiment_id="exp_x", platform="youtube", metric="ctr", value=0.08)
    obs_yield = Observation(experiment_id="exp_x", platform="youtube", metric="learning_yield", value=1.5)

    signals = classifier.classify_and_route([obs_error, obs_ctr, obs_yield], correlation_id="corr_c")
    assert len(signals) == 3
    assert signals[0].feedback_level == 1  # Operational
    assert signals[1].feedback_level == 2  # Performance
    assert signals[2].feedback_level == 5  # Evolutionary


def test_knowledge_engine_immutability_and_consolidation():
    """Verify KnowledgeEngine enforces ADR-004 immutability and FR-EC-104 consolidation."""
    ke = KnowledgeEngine()
    kr1 = KnowledgeRecord(
        type=KnowledgeType.FACT,
        statement="Title questions increase CTR by 10%",
        scope=Scope(niche="tech"),
        confidence=0.80,
        provenance=Provenance(source_id="exp_01", created_by_engine="Test"),
        status=KnowledgeStatus.ACTIVE,
        embedding_vector=[1.0, 0.0, 0.0]
    )
    kr2 = KnowledgeRecord(
        type=KnowledgeType.FACT,
        statement="Question titles boost click through by 12%",
        scope=Scope(niche="tech"),
        confidence=0.82,
        provenance=Provenance(source_id="exp_02", created_by_engine="Test"),
        status=KnowledgeStatus.ACTIVE,
        embedding_vector=[0.98, 0.1, 0.0]  # Very high cosine similarity to kr1
    )
    ke.add_record(kr1)
    ke.add_record(kr2)

    # Test consolidation
    events = ke.consolidate(similarity_threshold=0.85)
    assert len(events) == 1
    cons_id, id1, id2 = events[0]
    assert ke.get_record(id1).status == KnowledgeStatus.ARCHIVED
    assert ke.get_record(id2).status == KnowledgeStatus.ARCHIVED
    assert ke.get_record(cons_id).status == KnowledgeStatus.ACTIVE


def test_learning_and_reflection_pipeline():
    """Verify ReflectionEngine surprise scoring and LearningEngine lesson extraction + promotion."""
    ke = KnowledgeEngine()
    broker = MemoryBroker()
    le = LearningEngine(ke, broker=broker)
    re = ReflectionEngine(broker=broker)

    # Setup experiment with prediction
    mut = Mutation(experiment_id="exp_42", mutation_class="TOPIC", variable_id="var_1", baseline_value="A", mutated_value="B", justification="test")
    exp = Experiment(
        id="exp_42",
        strategy_id="strat_1",
        hypothesis_id="hyp_1",
        mutations=[mut],
        prediction=Prediction(experiment_id="exp_42", hypothesis_id="hyp_1", metric_predictions=[
            MetricPrediction(metric="selection_rate", expected_value=0.08, expected_range={"min": 0.07, "max": 0.09})
        ])
    )

    # Actual outcome is surprising (0.16 vs predicted 0.08 -> 100% relative delta)
    reflection = re.generate_reflection(exp, {"selection_rate": 0.16}, correlation_id="corr_re")
    assert reflection.surprise_score == 1.0  # High surprise

    # Extract lesson
    lessons = le.extract_lessons(reflection, correlation_id="corr_le")
    assert len(lessons) == 1
    kr_id = lessons[0].knowledge_record_id
    kr = ke.get_record(kr_id)
    assert kr.status == KnowledgeStatus.CANDIDATE

    # Test promotion guardrails (min_evidence_count = 3)
    assert le.evaluate_promotion(kr_id) is False  # Only 1 evidence ref currently

    # Add 2 more evidence refs
    kr.evidence_refs.extend(["exp_43", "exp_44"])
    assert le.evaluate_promotion(kr_id) is True  # Now promoted!
    assert kr.status == KnowledgeStatus.ACTIVE
