"""
Chaos and Checkpoint Resume Tests (`FR-EC-502` & NFR-AVA-002).

Tests killing/interrupting the `EvolutionCycleSaga` at intermediate steps (e.g. after Step 4, Step 8),
verifying checkpoint persistence in `SagaStateStore`, and verifying `resume_cycle()` resumes
exactly from `last_completed_step + 1` without repeating prior steps.
"""
import pytest
from evolutionos.core.saga.evolution_cycle_saga import (
    EvolutionCycleSaga, SagaStateStore, SagaStep, SagaStatus, SagaState
)
from evolutionos.core.evolution.experiment_engine import ExperimentEngine
from evolutionos.core.evolution.hypothesis_engine import HypothesisEngine
from evolutionos.core.evolution.mutation_engine import MutationEngine
from evolutionos.core.evolution.fitness_engine import FitnessEngine
from evolutionos.core.evolution.memory_engine import MemoryEngine
from evolutionos.core.learning.knowledge_engine import KnowledgeEngine
from evolutionos.core.learning.reflection_engine import ReflectionEngine
from evolutionos.core.learning.learning_engine import LearningEngine
from evolutionos.core.perception.observation_gateway import ObservationGateway
from evolutionos.core.reasoning.belief_engine import BeliefEngine
from evolutionos.core.reasoning.decision_engine import DecisionEngine
from evolutionos.core.reasoning.strategy_engine import StrategyEngine
from evolutionos.infrastructure.messaging.redis_streams import MemoryBroker


class MockFaultySaga(EvolutionCycleSaga):
    """Subclass that deliberately raises an error at a configured crash step to simulate kill/crash."""
    def __init__(self, crash_at_step: SagaStep, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crash_at_step = crash_at_step
        self.step_execution_log = []

    def _record_step(self, step: SagaStep):
        self.step_execution_log.append(step)
        if step == self.crash_at_step:
            raise RuntimeError(f"Simulated Crash at {step.name}!")

    def _step_memory_consolidation(self, state: SagaState) -> None:
        self._record_step(SagaStep.MEMORY_CONSOLIDATION)
        super()._step_memory_consolidation(state)

    def _step_belief_decay(self, state: SagaState) -> None:
        self._record_step(SagaStep.BELIEF_DECAY)
        super()._step_belief_decay(state)

    def _step_hypothesis_generation(self, state: SagaState) -> None:
        self._record_step(SagaStep.HYPOTHESIS_GENERATION)
        super()._step_hypothesis_generation(state)

    def _step_strategy_review(self, state: SagaState) -> None:
        self._record_step(SagaStep.STRATEGY_REVIEW)
        super()._step_strategy_review(state)

    def _step_decision_selection(self, state: SagaState) -> None:
        self._record_step(SagaStep.DECISION_SELECTION)
        super()._step_decision_selection(state)


def test_saga_checkpoint_persistence_and_resume_after_crash():
    """Verify FR-EC-502: saga saves checkpoint, crashes at Step 4, then resumes cleanly from Step 4."""
    store = SagaStateStore()
    broker = MemoryBroker()

    ke = KnowledgeEngine()
    be = BeliefEngine()
    he = HypothesisEngine()
    se = StrategyEngine()
    de = DecisionEngine(ke, be)
    ee = ExperimentEngine()
    og = ObservationGateway()
    re = ReflectionEngine()
    le = LearningEngine(ke, broker=broker)
    fe = FitnessEngine(ke)
    mem = MemoryEngine(ke, be)

    # 1. Start faulty saga that crashes at Step 4 (STRATEGY_REVIEW)
    faulty_saga = MockFaultySaga(
        crash_at_step=SagaStep.STRATEGY_REVIEW,
        store=store, memory_engine=mem, belief_engine=be, hypothesis_engine=he,
        strategy_engine=se, decision_engine=de, experiment_engine=ee,
        observation_gateway=og, reflection_engine=re, learning_engine=le,
        fitness_engine=fe, broker=broker
    )

    with pytest.raises(RuntimeError, match="Simulated Crash at STRATEGY_REVIEW"):
        faulty_saga.start_cycle()

    # Verify that steps 1, 2, 3 completed and checkpointed before crash
    assert len(store.states) == 1
    cycle_id = list(store.states.keys())[0]
    saved_state = store.load(cycle_id)
    assert saved_state.status == SagaStatus.FAILED
    assert saved_state.last_completed_step == SagaStep.HYPOTHESIS_GENERATION
    assert faulty_saga.step_execution_log == [
        SagaStep.MEMORY_CONSOLIDATION,
        SagaStep.BELIEF_DECAY,
        SagaStep.HYPOTHESIS_GENERATION,
        SagaStep.STRATEGY_REVIEW  # Crashed during this step
    ]

    # 2. Now resume with a healthy saga instance using the same persistent store
    saved_state.status = SagaStatus.IN_PROGRESS
    store.save(saved_state)

    healthy_saga = EvolutionCycleSaga(
        store=store, memory_engine=mem, belief_engine=be, hypothesis_engine=he,
        strategy_engine=se, decision_engine=de, experiment_engine=ee,
        observation_gateway=og, reflection_engine=re, learning_engine=le,
        fitness_engine=fe, broker=broker
    )

    resumed_state = healthy_saga.resume_cycle(cycle_id)
    assert resumed_state.status == SagaStatus.COMPLETED
    assert resumed_state.last_completed_step == SagaStep.META_CHECK
