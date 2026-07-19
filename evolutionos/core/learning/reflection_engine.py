"""
Reflection Engine (FR-EC-120, FR-EC-121, FR-EC-122).

Generates mandatory `ReflectionReport` for every terminal experiment, calculates surprise scores,
prioritizes high-surprise outcomes (>0.6) for learning, and performs periodic meta-reflection.
"""
import logging
from typing import Any, Dict, List, Optional
from evolutionos.core.domain.ontology import ReflectionReport, Experiment
from evolutionos.core.events.catalog import EventEnvelope
from evolutionos.infrastructure.messaging.broker import MessageBroker
from evolutionos.config.settings import settings

logger = logging.getLogger("evolutionos.reflection")


class ReflectionEngine:
    """Generates mandatory reflections, scores surprise, and triggers learning pipeline."""

    def __init__(self, broker: Optional[MessageBroker] = None):
        self.broker = broker
        self.reflections: Dict[str, ReflectionReport] = {}
        self.meta_reflection_counter = 0

    def generate_reflection(
        self,
        experiment: Experiment,
        actual_outcomes: Dict[str, float],
        correlation_id: str
    ) -> ReflectionReport:
        """FR-EC-120: Generate mandatory ReflectionReport comparing prediction against actual outcomes."""
        pred_map = {}
        if experiment.prediction and experiment.prediction.metric_predictions:
            for mp in experiment.prediction.metric_predictions:
                pred_map[mp.metric] = mp.expected_value

        per_metric_delta = {}
        surprise_scores = []

        for metric_name, actual_val in actual_outcomes.items():
            pred_val = pred_map.get(metric_name, actual_val)
            abs_delta = abs(actual_val - pred_val)
            rel_delta = (abs_delta / pred_val) if pred_val != 0 else (0.0 if actual_val == 0 else 1.0)
            within_range = rel_delta <= 0.15

            per_metric_delta[metric_name] = {
                "predicted": pred_val,
                "actual": actual_val,
                "absolute_delta": abs_delta,
                "relative_delta": rel_delta,
                "within_expected_range": within_range
            }
            # Surprise is high when relative delta is high
            surprise_scores.append(min(1.0, rel_delta))

        overall_surprise = max(surprise_scores) if surprise_scores else 0.0

        # Create attribution claims from mutations
        attributions = []
        for mut in experiment.mutations:
            attributions.append({
                "mutation_id": mut.id,
                "attributed_effect": per_metric_delta,
                "confidence": 0.70 if overall_surprise < 0.30 else 0.40
            })

        report = ReflectionReport(
            experiment_id=experiment.id,
            prediction={"metric_predictions": pred_map},
            actual=actual_outcomes,
            delta={"per_metric": per_metric_delta},
            surprise_score=overall_surprise,
            attribution=attributions,
            meta_notes=f"Surprise score: {overall_surprise:.2f}"
        )
        self.reflections[report.id] = report
        self.meta_reflection_counter += 1

        # FR-EC-121: Check if high surprise (>0.6) and prioritize in queue
        is_high_surprise = overall_surprise > 0.60
        if is_high_surprise:
            logger.info(f"High surprise ({overall_surprise:.2f}) detected for experiment {experiment.id}! Prioritizing.")

        # Emit ReflectionProduced event
        if self.broker:
            env = EventEnvelope(
                event_type="ReflectionProduced",
                correlation_id=correlation_id,
                producer="ReflectionEngine",
                payload={
                    "reflection_id": report.id,
                    "experiment_id": experiment.id,
                    "surprise_score": overall_surprise,
                    "high_surprise_priority": is_high_surprise
                }
            )
            self.broker.publish("core.events", env)

        # FR-EC-122: Check meta-reflection interval
        if self.meta_reflection_counter >= settings.meta_reflection_interval:
            self._perform_meta_reflection(correlation_id)

        return report

    def _perform_meta_reflection(self, correlation_id: str) -> None:
        logger.info(f"FR-EC-122: Performing meta-reflection across last {self.meta_reflection_counter} reflections.")
        self.meta_reflection_counter = 0
        if self.broker:
            env = EventEnvelope(
                event_type="SelfEvaluationTriggered",
                correlation_id=correlation_id,
                producer="ReflectionEngine",
                payload={"reason": "META_REFLECTION_INTERVAL_REACHED"}
            )
            self.broker.publish("engine.governance", env)
