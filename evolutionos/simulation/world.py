"""
Synthetic World (FR-EC-601, ADR-018).

Simulated environment with planted ground-truth rules and Gaussian noise (`stddev = 0.03`).
Translates experiment parameters into simulated observations and metrics (`ctr`, `retention`,
`conversion`, `performance_delta`) to verify Core cognitive discovery capability before real-world deployment.
"""
import random
from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from evolutionos.config.settings import settings


@dataclass
class PlantedRule:
    rule_id: str
    variable_name: str
    target_value: Any
    affected_metric: str
    effect_size: float  # e.g. +0.12 means +12% increase
    description: str


# 10 Planted Ground-Truth Rules (FR-EC-601 requirement: 8-12 rules)
DEFAULT_PLANTED_RULES: List[PlantedRule] = [
    PlantedRule("R1", "hook_type", "question", "ctr", 0.12, "Questions in hooks increase CTR by 12%"),
    PlantedRule("R2", "video_length", "8-12m", "retention", 0.15, "8-12 min videos increase retention by 15%"),
    PlantedRule("R3", "thumbnail_style", "high_contrast", "ctr", 0.08, "High contrast thumbnails boost CTR by 8%"),
    PlantedRule("R4", "pacing_speed", "fast", "retention", 0.10, "Fast pacing improves retention by 10%"),
    PlantedRule("R5", "call_to_action", "mid_roll", "conversion", 0.14, "Mid-roll CTAs boost conversion by 14%"),
    PlantedRule("R6", "title_format", "numbered_list", "ctr", 0.09, "Numbered list titles increase CTR by 9%"),
    PlantedRule("R7", "b_roll_density", "high", "retention", 0.11, "High B-roll density improves retention by 11%"),
    PlantedRule("R8", "audio_mastering", "crisp_vocal", "retention", 0.07, "Crisp vocal audio increases retention by 7%"),
    PlantedRule("R9", "topic_niche", "ai_tutorials", "ctr", 0.16, "AI tutorials niche boosts base CTR by 16%"),
    PlantedRule("R10", "posting_time", "morning_est", "ctr", 0.06, "Morning EST posting gives 6% CTR bump"),
]


class SyntheticWorld:
    """Simulates external environment responses to ExperimentDirectives based on planted rules."""

    def __init__(self, planted_rules: Optional[List[PlantedRule]] = None, noise_stddev: Optional[float] = None):
        self.rules = planted_rules if planted_rules is not None else DEFAULT_PLANTED_RULES
        self.noise_stddev = noise_stddev if noise_stddev is not None else settings.sim_noise_stddev
        self.base_metrics = {
            "ctr": 0.05,
            "retention": 0.40,
            "conversion": 0.02
        }

    def evaluate_parameters(self, parameters: Dict[str, Any]) -> Dict[str, float]:
        """Evaluate parameters against planted ground-truth rules with Gaussian noise."""
        outcomes = self.base_metrics.copy()
        performance_delta = 0.0

        # Check each planted rule against submitted parameters
        for rule in self.rules:
            val = parameters.get(rule.variable_name)
            if val == rule.target_value:
                # Apply positive effect
                if rule.affected_metric in outcomes:
                    outcomes[rule.affected_metric] += rule.effect_size
                performance_delta += rule.effect_size

        # Add Gaussian noise
        for m in outcomes:
            noise = random.gauss(0.0, self.noise_stddev)
            outcomes[m] = max(0.001, min(0.999, outcomes[m] + noise))

        outcomes["performance_delta"] = round(performance_delta, 4)
        return outcomes

    def get_ground_truth_rule_ids(self) -> set:
        return {r.rule_id for r in self.rules}
