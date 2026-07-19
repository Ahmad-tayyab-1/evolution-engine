"""
Mutation Engine (FR-EC-420, FR-EC-421, FR-EC-422).

Enforces canonical mutation taxonomy (`TOPIC`, `STRUCTURE`, `PRESENTATION`, `TIMING`,
`SCOPE`, `META`). Enforces mutation budget (`default_mutation_budget = 1`; exceeding budget
requires explicit justification). Enforces distance scoring across portfolio distribution.
"""
from typing import Any, Dict, List, Optional
from evolutionos.core.domain.ontology import Mutation
from evolutionos.config.settings import settings

# Legal mutation classes (FR-EC-420)
VALID_MUTATION_CLASSES = {"TOPIC", "STRUCTURE", "PRESENTATION", "TIMING", "SCOPE", "META"}
# Legal mutation distance categories (FR-EC-422)
VALID_DISTANCES = {"NEAR", "MID", "FAR"}


class MutationEngine:
    """Enforces taxonomy, mutation budget, and distance distribution across experiments."""

    def __init__(self):
        self.mutations: Dict[str, Mutation] = {}

    def create_mutation(
        self,
        experiment_id: str,
        mutation_class: str,
        variable_id: str,
        baseline_value: Any,
        mutated_value: Any,
        justification: str,
        distance: str = "NEAR"
    ) -> Mutation:
        """FR-EC-420 & FR-EC-422: Validate and create mutation."""
        if mutation_class not in VALID_MUTATION_CLASSES:
            raise ValueError(f"FR-EC-420 Violation: Invalid mutation class '{mutation_class}'. Must be one of {VALID_MUTATION_CLASSES}.")
        if distance not in VALID_DISTANCES:
            raise ValueError(f"FR-EC-422 Violation: Invalid distance '{distance}'. Must be one of {VALID_DISTANCES}.")
        if not justification or len(justification.strip()) < 5:
            raise ValueError("Mutation requires clear justification.")

        # Enforce ADR-019: Meta-mutations (self-modifications) execute in shadow mode first
        eval_mode = "SHADOW" if mutation_class == "META" else "LIVE"

        mut = Mutation(
            experiment_id=experiment_id,
            mutation_class=mutation_class,
            variable_id=variable_id,
            baseline_value=baseline_value,
            mutated_value=mutated_value,
            justification=justification,
            distance=distance,
            evaluation_mode=eval_mode
        )
        self.mutations[mut.id] = mut
        return mut

    def evaluate_shadow_mutation(self, mutation_id: str, historical_replay_passed: bool) -> bool:
        """ADR-019: Promote shadow meta-mutation to LIVE if historical replay check passed."""
        if mutation_id not in self.mutations:
            raise ValueError(f"Mutation {mutation_id} not found.")
        mut = self.mutations[mutation_id]
        if mut.evaluation_mode != "SHADOW":
            return True
        if historical_replay_passed:
            mut.evaluation_mode = "LIVE"
            return True
        return False

    def validate_budget(self, mutations: List[Mutation], budget: Optional[int] = None) -> bool:
        """FR-EC-421: Verify mutations do not exceed budget without explicit justification (`DP-011`)."""
        max_budget = budget if budget is not None else settings.default_mutation_budget
        if len(mutations) > max_budget:
            # Check if all mutations beyond budget have multi-variable explicit justification
            for m in mutations:
                if "multi-variable" not in m.justification.lower() and "exceed" not in m.justification.lower():
                    raise ValueError(
                        f"FR-EC-421 Violation: {len(mutations)} mutations exceed budget ({max_budget}) without explicit justification."
                    )
        return True

    def get_portfolio_distance_distribution(self, active_experiment_ids: set) -> Dict[str, float]:
        """FR-EC-422: Calculate distribution of NEAR vs MID vs FAR across active portfolio."""
        active_muts = [m for m in self.mutations.values() if m.experiment_id in active_experiment_ids]
        if not active_muts:
            return {"NEAR": 0.0, "MID": 0.0, "FAR": 0.0}

        counts = {"NEAR": 0, "MID": 0, "FAR": 0}
        for m in active_muts:
            counts[m.distance] = counts.get(m.distance, 0) + 1

        total = len(active_muts)
        return {k: round(v / total, 2) for k, v in counts.items()}
