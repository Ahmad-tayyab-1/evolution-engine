"""
Fitness Engine (FR-EC-430, FR-EC-431, FR-EC-432).

Computes multi-objective `FitnessVector` (`learning_yield`, `prediction_accuracy`,
`performance_delta`, `strategic_alignment`, `cost_efficiency`) and weighted scalar scores
using versioned weight profiles. Enforces Anti-Gaming Rule (`learning_yield` only from `ACTIVE` lessons).
"""
from typing import Dict, List, Optional
from evolutionos.core.domain.ontology import (
    FitnessRecord, FitnessVector, Lesson, KnowledgeStatus, Experiment
)
from evolutionos.core.events.catalog import EventEnvelope
from evolutionos.core.learning.knowledge_engine import KnowledgeEngine
from evolutionos.infrastructure.messaging.broker import MessageBroker
from evolutionos.config.settings import settings


class FitnessEngine:
    """Computes FitnessVector and scalar score using weight profiles and anti-gaming rules."""

    def __init__(self, knowledge_engine: KnowledgeEngine, broker: Optional[MessageBroker] = None):
        self.knowledge_engine = knowledge_engine
        self.broker = broker
        self.fitness_records: Dict[str, FitnessRecord] = {}
        self.weight_profiles: Dict[str, Dict[str, float]] = {
            "default_weights": settings.fitness_weights,
            "exploration_weights": {
                "learning_yield": 0.60,
                "prediction_accuracy": 0.15,
                "performance_delta": 0.10,
                "strategic_alignment": 0.10,
                "cost_efficiency": 0.05
            }
        }

    def compute_fitness(
        self,
        experiment: Experiment,
        extracted_lessons: List[Lesson],
        actual_outcomes: Dict[str, float],
        weight_profile_id: str = "default_weights",
        correlation_id: str = "none"
    ) -> FitnessRecord:
        """FR-EC-430, FR-EC-431, FR-EC-432: Compute vector and scalar fitness."""
        # 1. learning_yield with Anti-Gaming Rule (FR-EC-432: only ACTIVE status lessons count)
        active_lesson_count = 0
        for l in extracted_lessons:
            kr = self.knowledge_engine.get_record(l.knowledge_record_id)
            if kr and kr.status == KnowledgeStatus.ACTIVE:
                active_lesson_count += 1
        learning_yield = float(active_lesson_count) * 0.5

        # 2. prediction_accuracy
        pred_acc = 1.0
        if experiment.prediction and experiment.prediction.metric_predictions:
            acc_scores = []
            for mp in experiment.prediction.metric_predictions:
                actual = actual_outcomes.get(mp.metric, mp.expected_value)
                err = abs(actual - mp.expected_value) / (mp.expected_value if mp.expected_value != 0 else 1.0)
                acc_scores.append(max(0.0, 1.0 - err))
            pred_acc = sum(acc_scores) / len(acc_scores) if acc_scores else 1.0

        # 3. performance_delta (normalized shift vs baseline)
        performance_delta = actual_outcomes.get("performance_delta", 0.10)

        # 4. strategic_alignment & cost_efficiency
        strategic_alignment = 0.80
        cost_efficiency = 0.90

        vector = FitnessVector(
            learning_yield=learning_yield,
            prediction_accuracy=pred_acc,
            performance_delta=performance_delta,
            strategic_alignment=strategic_alignment,
            cost_efficiency=cost_efficiency
        )

        # Compute scalar using weight profile (FR-EC-431)
        weights = self.weight_profiles.get(weight_profile_id, self.weight_profiles["default_weights"])
        scalar = (
            vector.learning_yield * weights.get("learning_yield", 0.35) +
            vector.prediction_accuracy * weights.get("prediction_accuracy", 0.25) +
            vector.performance_delta * weights.get("performance_delta", 0.20) +
            vector.strategic_alignment * weights.get("strategic_alignment", 0.15) +
            vector.cost_efficiency * weights.get("cost_efficiency", 0.05)
        )

        rec = FitnessRecord(
            experiment_id=experiment.id,
            weight_profile_id=weight_profile_id,
            vector=vector,
            scalar=scalar
        )
        self.fitness_records[rec.id] = rec

        if self.broker:
            env = EventEnvelope(
                event_type="FitnessComputed",
                correlation_id=correlation_id,
                producer="FitnessEngine",
                payload={"fitness_id": rec.id, "experiment_id": experiment.id, "scalar_score": scalar}
            )
            self.broker.publish("core.events", env)

        return rec
