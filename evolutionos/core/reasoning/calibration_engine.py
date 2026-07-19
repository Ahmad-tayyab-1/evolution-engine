"""
Calibration & Goodhart Defense (`ADR-020`, `SIM-001`).

Mitigates Goodhart's Law ("When a measure becomes a target, it ceases to be a good measure").
Monitors calibration accuracy (Brier score / confidence error) across `Belief`s and `Lesson`s,
and detects degenerate gaming of `FitnessVector` metrics (`learning_yield` and `prediction_accuracy`).
"""
import logging
from typing import Dict, Any, List, Optional, Tuple
from evolutionos.core.domain.ontology import (
    Lesson, KnowledgeRecord, Belief, FitnessRecord, FitnessVector
)
from evolutionos.core.learning.knowledge_engine import KnowledgeEngine
from evolutionos.config.settings import settings

logger = logging.getLogger("evolutionos.core.reasoning.calibration")


class GoodhartViolationType(str):
    INFLATED_LEARNING_YIELD = "INFLATED_LEARNING_YIELD"
    TRIVIAL_PREDICTION_GAMING = "TRIVIAL_PREDICTION_GAMING"
    UNCALIBRATED_CONFIDENCE_SPAM = "UNCALIBRATED_CONFIDENCE_SPAM"


class CalibrationResult:
    def __init__(
        self,
        brier_score: float,
        mean_calibration_error: float,
        is_calibrated: bool,
        goodhart_penalty_factor: float,
        violations: List[str]
    ):
        self.brier_score = round(brier_score, 4)
        self.mean_calibration_error = round(mean_calibration_error, 4)
        self.is_calibrated = is_calibrated
        self.goodhart_penalty_factor = round(goodhart_penalty_factor, 4)
        self.violations = violations


class CalibrationEngine:
    """Enforces Brier score bounds and defends against Goodhart gaming (`ADR-020`)."""

    def __init__(self, knowledge_engine: Optional[KnowledgeEngine] = None):
        self.ke = knowledge_engine

    def compute_brier_score(self, predictions_and_outcomes: List[Tuple[float, float]]) -> float:
        """Calculate Brier score across (confidence, empirical_outcome) pairs where outcome is 1.0 (success) or 0.0 (failure)."""
        if not predictions_and_outcomes:
            return 0.0
        mse = sum((conf - outcome) ** 2 for conf, outcome in predictions_and_outcomes) / len(predictions_and_outcomes)
        return mse

    def evaluate_calibration_and_goodhart_defense(
        self,
        extracted_lessons: List[Lesson],
        predictions_and_outcomes: List[Tuple[float, float]],
        fitness_vector: FitnessVector
    ) -> CalibrationResult:
        """Evaluate calibration bounds (`max_calibration_error = 0.15`) and detect Goodhart gaming (`ADR-020`)."""
        violations = []
        goodhart_penalty = 1.0

        # 1. Brier Score & Mean Calibration Error
        brier = self.compute_brier_score(predictions_and_outcomes)
        if predictions_and_outcomes:
            mean_error = sum(abs(conf - outcome) for conf, outcome in predictions_and_outcomes) / len(predictions_and_outcomes)
        else:
            mean_error = 0.0

        is_calibrated = mean_error <= settings.sim_max_calibration_error

        if not is_calibrated:
            violations.append(GoodhartViolationType.UNCALIBRATED_CONFIDENCE_SPAM)
            # Apply penalty proportional to excess calibration error
            excess_err = mean_error - settings.sim_max_calibration_error
            goodhart_penalty *= max(0.2, 1.0 - (excess_err * 2.0))
            logger.warning(f"ADR-020 Violation: Uncalibrated confidence (error={mean_error:.4f} > {settings.sim_max_calibration_error}). Penalty={goodhart_penalty}")

        # 2. Check for Inflated Learning Yield Gaming (e.g. generating duplicate lessons just to pump yield)
        if self.ke and len(extracted_lessons) >= 3:
            statements = []
            for l in extracted_lessons:
                kr = self.ke.get_record(l.knowledge_record_id)
                if kr:
                    statements.append(kr.statement.lower().strip())

            # Check exact or near duplicates among lessons in a single cycle
            unique_statements = set(statements)
            if len(unique_statements) < len(statements) * 0.75:
                violations.append(GoodhartViolationType.INFLATED_LEARNING_YIELD)
                goodhart_penalty *= 0.5
                logger.warning(f"ADR-020 Violation: Diminishing entropy / duplicate lessons detected ({len(unique_statements)} unique / {len(statements)} total). Penalty applied.")

        # 3. Check for Trivial Prediction Gaming (e.g., prediction accuracy = 1.0 while performance delta <= 0.0)
        if fitness_vector.prediction_accuracy >= 0.98 and fitness_vector.performance_delta <= 0.0:
            # If accuracy is suspiciously perfect without driving real performance improvements over multiple cycles
            violations.append(GoodhartViolationType.TRIVIAL_PREDICTION_GAMING)
            goodhart_penalty *= 0.8

        return CalibrationResult(
            brier_score=brier,
            mean_calibration_error=mean_error,
            is_calibrated=is_calibrated,
            goodhart_penalty_factor=goodhart_penalty,
            violations=violations
        )

    def apply_goodhart_adjustment(self, fitness_record: FitnessRecord, calibration_result: CalibrationResult) -> FitnessRecord:
        """Adjust scalar fitness score by applying the Goodhart penalty factor (`ADR-020`)."""
        if calibration_result.goodhart_penalty_factor < 1.0:
            original_scalar = fitness_record.scalar
            fitness_record.scalar = round(original_scalar * calibration_result.goodhart_penalty_factor, 4)
            logger.info(f"ADR-020 Goodhart adjustment applied to experiment [{fitness_record.experiment_id}]: scalar {original_scalar} -> {fitness_record.scalar}")
        return fitness_record
