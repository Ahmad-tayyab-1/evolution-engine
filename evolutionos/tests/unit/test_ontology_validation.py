"""
Unit tests verifying Level 0-6 canonical ontology validation rules and bounds (`ONT-001`).
"""
import pytest
from pydantic import ValidationError
from evolutionos.core.domain.ontology import (
    Scope, Variable, VariableType, Metric, AggregationType,
    Observation, ObservationQuality, FeedbackSignal,
    KnowledgeRecord, KnowledgeType, Provenance,
    Belief, FalsifiableForm, Hypothesis, Candidate, Decision,
    Mutation, Experiment, ExperimentClass, ReflectionReport, FitnessRecord
)


def test_scope_compatibility_and_specificity():
    """Verify Scope specificity calculation and compatibility matching."""
    s1 = Scope(niche="cybersecurity", format="long")
    s2 = Scope(niche="cybersecurity")
    s3 = Scope(niche="gaming")

    assert s1.specificity_score() == 2
    assert s2.specificity_score() == 1
    assert s1.is_compatible_with(s2) is True
    assert s1.is_compatible_with(s3) is False


def test_variable_invariants():
    """Verify Variable must be either manipulable or observable."""
    v1 = Variable(name="hook_type", label="Hook Type", type=VariableType.CATEGORICAL, is_manipulable=True)
    assert v1.name == "hook_type"

    with pytest.raises(ValidationError, match="Variable invariant: must be either manipulable or observable"):
        Variable(name="dead_var", label="Dead", type=VariableType.CONTINUOUS, is_manipulable=False, is_observable=False)


def test_knowledge_record_and_confidence_bounds():
    """Verify KnowledgeRecord bounds (`CON-ETH-003` - never 0 or 1)."""
    kr = KnowledgeRecord(
        type=KnowledgeType.FACT,
        statement="3-minute intros have 67% average retention",
        confidence=0.85,
        provenance=Provenance(source_id="exp_123", created_by_engine="LearningEngine")
    )
    assert kr.confidence == 0.85

    with pytest.raises(ValidationError):
        KnowledgeRecord(
            type=KnowledgeType.FACT,
            statement="Certainty claimed",
            confidence=1.0,  # Illegal under CON-ETH-003
            provenance=Provenance(source_id="exp_123", created_by_engine="LearningEngine")
        )


def test_hypothesis_falsifiability_structure():
    """Verify Hypothesis requires complete FalsifiableForm."""
    hyp = Hypothesis(
        formal_form=FalsifiableForm(
            if_variable="var_hook",
            changes_from="statistic",
            changes_to="question",
            in_scope=Scope(niche="science"),
            then_metric="selection_rate",
            change_direction="INCREASE"
        )
    )
    assert hyp.formal_form.if_variable == "var_hook"
    assert hyp.status == "PROPOSED"


def test_experiment_and_mutation():
    """Verify Experiment and Mutation model creation."""
    mut = Mutation(
        experiment_id="exp_001",
        mutation_class="TOPIC",
        variable_id="var_topic",
        baseline_value="Old Topic",
        mutated_value="New Topic",
        justification="Testing audience interest"
    )
    assert mut.mutation_class == "TOPIC"

    exp = Experiment(
        strategy_id="strat_99",
        hypothesis_id="hyp_88",
        experiment_class=ExperimentClass.EXPLORATORY,
        mutations=[mut]
    )
    assert exp.experiment_class == ExperimentClass.EXPLORATORY
    assert len(exp.mutations) == 1
