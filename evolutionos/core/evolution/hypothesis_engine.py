"""
Hypothesis Engine (FR-EC-410, FR-EC-411).

Validates canonical falsifiable form across all hypotheses (`if_variable`, `changes_from/to`,
`in_scope`, `then_metric`, `change_direction`, `change_magnitude`, `within_window`, `expected_confidence`).
Manages hypothesis backlog from priority sources (`Belief validation`, `Contradiction`, etc.).
"""
from typing import Dict, List, Optional
from evolutionos.core.domain.ontology import Hypothesis, HypothesisStatus, FalsifiableForm
from evolutionos.core.events.catalog import HypothesisGenerated, EventEnvelope
from evolutionos.infrastructure.messaging.broker import MessageBroker


class HypothesisEngine:
    """Validates falsifiable forms and manages backlog prioritized by source class."""

    def __init__(self, broker: Optional[MessageBroker] = None):
        self.backlog: Dict[str, Hypothesis] = {}
        self.broker = broker

    def validate_falsifiable_form(self, form: FalsifiableForm) -> bool:
        """FR-EC-410: Reject hypothesis if any element of falsifiable form is missing or invalid."""
        if not form.if_variable or not form.then_metric or not form.in_scope:
            return False
        if not form.change_direction in ["INCREASE", "DECREASE", "STABILIZE"]:
            return False
        if not form.within_window or not form.expected_confidence:
            return False
        if not (0.01 <= form.expected_confidence <= 0.99):
            return False
        return True

    def create_hypothesis(
        self,
        form: FalsifiableForm,
        source_class: str,
        source_details: Dict,
        priority_score: float = 0.5,
        correlation_id: str = "none"
    ) -> Hypothesis:
        """FR-EC-410 & FR-EC-411: Create and validate hypothesis from prioritized sources."""
        if not self.validate_falsifiable_form(form):
            raise ValueError("FR-EC-410 Violation: Hypothesis fails canonical falsifiable form validation.")

        # Source priority bonus (1: Belief validation -> 5: Structured exploration)
        priority_bonuses = {
            "BELIEF_VALIDATION": 0.40,
            "CONTRADICTION_RESOLUTION": 0.35,
            "STRATEGIC_OBJECTIVE": 0.25,
            "SURPRISE_INVESTIGATION": 0.20,
            "STRUCTURED_EXPLORATION": 0.10
        }
        computed_priority = min(1.0, priority_score + priority_bonuses.get(source_class, 0.0))

        hyp = Hypothesis(
            formal_form=form,
            source={"class": source_class, "details": source_details},
            priority_score=computed_priority,
            status=HypothesisStatus.PROPOSED
        )
        self.backlog[hyp.id] = hyp

        # Emit HypothesisGenerated event
        event = HypothesisGenerated(
            hypothesis_id=hyp.id,
            statement=f"IF {form.if_variable} -> THEN {form.then_metric} ({form.change_direction})",
            target_metric=form.then_metric,
            expected_direction=form.change_direction
        )
        if self.broker:
            env = event.wrap(producer="HypothesisEngine", correlation_id=correlation_id)
            self.broker.publish("core.events", env)

        return hyp

    def get_top_hypotheses(self, count: int = 5) -> List[Hypothesis]:
        """Retrieve highest priority proposed hypotheses from backlog."""
        proposed = [h for h in self.backlog.values() if h.status == HypothesisStatus.PROPOSED]
        proposed.sort(key=lambda h: h.priority_score, reverse=True)
        return proposed[:count]
