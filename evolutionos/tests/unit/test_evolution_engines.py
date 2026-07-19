"""
Unit tests for Phase 3 Evolution Engines (`FR-EC-401` through `FR-EC-441`).
"""
import pytest
from evolutionos.core.domain.ontology import (
    Experiment, ExperimentState, ExperimentClass, Hypothesis, HypothesisStatus,
    FalsifiableForm, Scope, Mutation, Lesson, KnowledgeRecord, KnowledgeType, KnowledgeStatus, Provenance
)
from evolutionos.core.evolution.experiment_engine import ExperimentEngine
from evolutionos.core.evolution.hypothesis_engine import HypothesisEngine
from evolutionos.core.evolution.mutation_engine import MutationEngine
from evolutionos.core.evolution.fitness_engine import FitnessEngine
from evolutionos.core.evolution.memory_engine import MemoryEngine
from evolutionos.core.learning.knowledge_engine import KnowledgeEngine
from evolutionos.core.reasoning.belief_engine import BeliefEngine
from evolutionos.infrastructure.messaging.redis_streams import MemoryBroker


def test_experiment_engine_state_machine_and_directive():
    """Verify state transitions (`FR-EC-401`) and SCHEDULED hypothesis requirement."""
    broker = MemoryBroker()
    ee = ExperimentEngine(broker=broker)

    exp = Experiment(strategy_id="s1", hypothesis_id="none", experiment_class=ExperimentClass.EXPLORATORY)
    exp_id = ee.add_experiment(exp)

    # Transition DRAFT -> HYPOTHESIZED -> APPROVED
    ee.transition_state(exp_id, ExperimentState.HYPOTHESIZED)
    ee.transition_state(exp_id, ExperimentState.APPROVED)

    # Attempting SCHEDULED without valid hypothesis should raise ValueError
    with pytest.raises(ValueError, match="SCHEDULED state requires an attached Hypothesis"):
        ee.transition_state(exp_id, ExperimentState.SCHEDULED)

    # Attach valid hypothesis
    hyp = Hypothesis(
        id="h1",
        formal_form=FalsifiableForm(if_variable="v", changes_from=1, changes_to=2, in_scope=Scope(), then_metric="ctr", change_direction="INCREASE"),
        status=HypothesisStatus.ACTIVE
    )
    ee.transition_state(exp_id, ExperimentState.SCHEDULED, hypothesis=hyp)
    assert ee.get_experiment(exp_id).state == ExperimentState.SCHEDULED

    # Issue directive (`FR-EC-402`)
    directive = ee.issue_directive(exp_id, {"topic": "AI"}, {"window": "24h"})
    assert directive.experiment_id == exp_id
    assert ee.get_experiment(exp_id).directive is not None


def test_hypothesis_and_mutation_engines():
    """Verify Hypothesis validation (`FR-EC-410`) and Mutation budget/distance (`FR-EC-420-422`)."""
    he = HypothesisEngine()
    me = MutationEngine()

    # Valid hypothesis
    form = FalsifiableForm(
        if_variable="title_format",
        changes_from="statement",
        changes_to="question",
        in_scope=Scope(niche="gaming"),
        then_metric="selection_rate",
        change_direction="INCREASE",
        within_window="48h",
        expected_confidence=0.80
    )
    hyp = he.create_hypothesis(form, source_class="BELIEF_VALIDATION", source_details={})
    assert hyp.status == HypothesisStatus.PROPOSED
    assert hyp.priority_score > 0.50

    # Valid mutation creation (`FR-EC-420` & `FR-EC-422`)
    m1 = me.create_mutation("exp_1", "TOPIC", "var_1", "old", "new", "testing audience interest", distance="MID")
    assert m1.distance == "MID"

    # Budget check (`FR-EC-421`)
    assert me.validate_budget([m1], budget=1) is True


def test_fitness_and_memory_engines():
    """Verify Fitness Anti-Gaming (`FR-EC-432`) and Memory consolidation (`FR-EC-440/441`)."""
    ke = KnowledgeEngine()
    be = BeliefEngine()
    fe = FitnessEngine(ke)
    mem = MemoryEngine(ke, be)

    # Add 1 ACTIVE lesson and 1 CANDIDATE lesson
    prov = Provenance(source_id="test_exp", created_by_engine="test")
    kr_active = KnowledgeRecord(type=KnowledgeType.LESSON, statement="Active lesson", confidence=0.8, status=KnowledgeStatus.ACTIVE, provenance=prov)
    kr_cand = KnowledgeRecord(type=KnowledgeType.LESSON, statement="Candidate lesson", confidence=0.5, status=KnowledgeStatus.CANDIDATE, provenance=prov)
    id_active = ke.add_record(kr_active)
    id_cand = ke.add_record(kr_cand)

    l_active = Lesson(knowledge_record_id=id_active, experiment_id="exp_99", dimension="ctr", claim="Active", confidence_at_creation=0.8)
    l_cand = Lesson(knowledge_record_id=id_cand, experiment_id="exp_99", dimension="ctr", claim="Candidate", confidence_at_creation=0.5)

    exp = Experiment(strategy_id="s1", hypothesis_id="h1", experiment_class=ExperimentClass.EXPLORATORY)
    rec = fe.compute_fitness(exp, [l_active, l_cand], {"performance_delta": 0.20})

    # Under Anti-Gaming Rule (`FR-EC-432`), only active lesson counts toward learning_yield
    assert rec.vector.learning_yield == 0.5  # 1 active lesson * 0.5

    # Memory consolidation check (`FR-EC-440`)
    summary = mem.run_consolidation_cycle()
    assert "consolidated_count" in summary


def test_mutation_engine_adr_019_shadow_mode():
    """Verify ADR-019: META mutations start in SHADOW mode and require replay pass to promote to LIVE."""
    me = MutationEngine()
    # Regular mutation defaults to LIVE
    m_reg = me.create_mutation("exp_1", "TOPIC", "var_1", "old", "new", "topic test")
    assert m_reg.evaluation_mode == "LIVE"

    # META mutation starts in SHADOW mode (`ADR-019`)
    m_meta = me.create_mutation("exp_2", "META", "learning_rate", 0.01, 0.05, "adjusting learning speed based on plateau")
    assert m_meta.evaluation_mode == "SHADOW"

    # Evaluate shadow mutation
    assert me.evaluate_shadow_mutation(m_meta.id, historical_replay_passed=False) is False
    assert m_meta.evaluation_mode == "SHADOW"

    assert me.evaluate_shadow_mutation(m_meta.id, historical_replay_passed=True) is True
    assert m_meta.evaluation_mode == "LIVE"
