"""
Unit tests for Phase 2 Reasoning Engines (`FR-EC-201` through `FR-EC-221`).
"""
import pytest
from datetime import datetime, timezone, timedelta
from evolutionos.core.domain.ontology import (
    Belief, BeliefStatus, Candidate, Strategy, StrategyStatus, Scope
)
from evolutionos.core.reasoning.belief_engine import BeliefEngine
from evolutionos.core.reasoning.decision_engine import DecisionEngine
from evolutionos.core.reasoning.strategy_engine import StrategyEngine
from evolutionos.core.learning.knowledge_engine import KnowledgeEngine
from evolutionos.infrastructure.messaging.redis_streams import MemoryBroker


def test_belief_engine_bayesian_update_and_decay():
    """Verify Bayesian-inspired confidence update (`FR-EC-202`) and 90-day decay (`FR-EC-203`)."""
    broker = MemoryBroker()
    be = BeliefEngine(broker=broker)

    belief = Belief(
        statement="Video length between 8-12m optimizes ad revenue and retention",
        confidence=0.50,
        status=BeliefStatus.ACTIVE
    )
    b_id = be.add_belief(belief)

    # Positive evidence update
    updated = be.update_confidence(b_id, direction=+1, evidence_weight=0.20, trigger="TEST_SUPPORTS")
    assert updated.confidence > 0.50
    assert len(updated.confidence_history) == 1

    # Test decay of unvalidated belief (>90 days old)
    old_timestamp = (datetime.now(timezone.utc) - timedelta(days=95)).isoformat()
    updated.last_validated_at = old_timestamp
    updated.confidence_history[0].timestamp = old_timestamp

    stale_ids = be.apply_decay()
    assert b_id in stale_ids
    assert updated.confidence < 0.54  # Decayed toward 0.5


def test_decision_engine_protocol_and_candidates():
    """Verify 8-step decision protocol (`FR-EC-210`) requires >=3 candidates and logs DecisionRecord (`FR-EC-211`)."""
    ke = KnowledgeEngine()
    be = BeliefEngine()
    de = DecisionEngine(ke, be)

    # Try making decision with < 3 candidates -> should raise ValueError
    with pytest.raises(ValueError, match="At least 3 candidates required"):
        de.make_decision(
            decision_type="TOPIC_SELECTION",
            context={"experiment_id": "exp_1"},
            candidates=[Candidate(type="topic", value="A", score=0.8)]
        )

    # Provide 3 valid candidates
    c1 = Candidate(id="c1", type="topic", value="Rust vs C++", score=0.90, risk=0.1)
    c2 = Candidate(id="c2", type="topic", value="Go vs Python", score=0.85, risk=0.2)
    c3 = Candidate(id="c3", type="topic", value="Assembler 101", score=0.60, risk=0.8)

    # Force EXPLOIT mode by setting exploration_rate = 0.0
    de.exploration_rate = 0.0
    dec = de.make_decision(
        decision_type="TOPIC_SELECTION",
        context={"experiment_id": "exp_1"},
        candidates=[c1, c2, c3],
        prediction_spec={"selection_rate": 0.12}
    )

    assert dec.selected_candidate_id == "c1"  # Highest score in exploit mode
    assert dec.policy == "EXPLOIT"
    assert dec.prediction is not None
    assert dec.prediction.metric_predictions[0].metric == "selection_rate"
    assert "c2" in dec.rejection_reasons
    assert "c3" in dec.rejection_reasons


def test_strategy_engine_lifecycle_and_review_trigger():
    """Verify StrategyEngine check_review_triggers (`FR-EC-221`) moves declining strategy to UNDER_REVIEW."""
    se = StrategyEngine()
    strat = Strategy(
        objective={"goal": "Double subscriber conversion rate"},
        status=StrategyStatus.ACTIVE,
        expiration={"type": "EXPERIMENT_COUNT", "value": 5},
        active_experiments=["exp_1", "exp_2", "exp_3", "exp_4", "exp_5"]  # Reached max experiments!
    )
    s_id = se.add_strategy(strat)

    triggered = se.check_review_triggers(s_id)
    assert triggered is True
    assert se.get_strategy(s_id).status == StrategyStatus.UNDER_REVIEW
