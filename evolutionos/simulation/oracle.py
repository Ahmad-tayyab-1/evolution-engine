"""
Ground Truth Oracle (`Plan.md` Section 6 / Appendix B).
Verifies synthetic simulation outputs against planted ground truth causal rules (`SIM-001`).
"""
from typing import Dict, Any, List
from evolutionos.simulation.world import SyntheticWorld


class SimulationOracle:
    """Verifies discovered rules against ground truth world (`SIM-001`)."""

    def __init__(self, world: SyntheticWorld):
        self.world = world

    def verify_discovery(self, if_var: str, then_metric: str, direction: str) -> Dict[str, Any]:
        """Check if proposed rule matches planted ground truth in SyntheticWorld."""
        for planted in self.world.ground_truth_rules:
            if planted.if_variable == if_var and planted.then_metric == then_metric and planted.change_direction == direction:
                return {
                    "is_true_positive": True,
                    "planted_rule": planted.model_dump(),
                    "expected_delta": planted.expected_delta
                }
        return {"is_true_positive": False, "planted_rule": None, "expected_delta": 0.0}
