"""
Experiment Engine (FR-EC-401, FR-EC-402).

Manages Experiment lifecycle state transitions (`DRAFT -> HYPOTHESIZED -> APPROVED ->
SCHEDULED -> EXECUTING -> MEASURING -> COMPLETED/FAILED -> REFLECTED -> ARCHIVED`).
Enforces rule that SCHEDULED requires a falsifiable Hypothesis.
Issues `ExperimentDirective` via domain event (`ExperimentDirectiveIssued`).
"""
import logging
from typing import Dict, List, Optional
from evolutionos.core.domain.ontology import (
    Experiment, ExperimentState, ExperimentDirective, Hypothesis, HypothesisStatus
)
from evolutionos.core.events.catalog import ExperimentDirectiveIssued, EventEnvelope
from evolutionos.infrastructure.messaging.broker import MessageBroker

logger = logging.getLogger("evolutionos.evolution.experiment")

# Legal state transitions map
VALID_TRANSITIONS: Dict[ExperimentState, List[ExperimentState]] = {
    ExperimentState.DRAFT: [ExperimentState.HYPOTHESIZED, ExperimentState.ARCHIVED],
    ExperimentState.HYPOTHESIZED: [ExperimentState.APPROVED, ExperimentState.DRAFT, ExperimentState.ARCHIVED],
    ExperimentState.APPROVED: [ExperimentState.SCHEDULED, ExperimentState.ARCHIVED],
    ExperimentState.SCHEDULED: [ExperimentState.EXECUTING, ExperimentState.ARCHIVED],
    ExperimentState.EXECUTING: [ExperimentState.MEASURING, ExperimentState.FAILED],
    ExperimentState.MEASURING: [ExperimentState.COMPLETED, ExperimentState.FAILED],
    ExperimentState.COMPLETED: [ExperimentState.REFLECTED],
    ExperimentState.FAILED: [ExperimentState.REFLECTED],
    ExperimentState.REFLECTED: [ExperimentState.ARCHIVED],
    ExperimentState.ARCHIVED: []  # Terminal
}


class ExperimentEngine:
    """Manages experiment state machine and directive issuance."""

    def __init__(self, broker: Optional[MessageBroker] = None):
        self.experiments: Dict[str, Experiment] = {}
        self.broker = broker

    def add_experiment(self, experiment: Experiment) -> str:
        self.experiments[experiment.id] = experiment
        return experiment.id

    def get_experiment(self, exp_id: str) -> Optional[Experiment]:
        return self.experiments.get(exp_id)

    def transition_state(
        self,
        exp_id: str,
        new_state: ExperimentState,
        hypothesis: Optional[Hypothesis] = None,
        correlation_id: str = "none"
    ) -> Experiment:
        """FR-EC-401: Enforce valid lifecycle transitions and rules."""
        exp = self.get_experiment(exp_id)
        if not exp:
            raise ValueError(f"Experiment {exp_id} not found.")

        old_state = exp.state
        allowed = VALID_TRANSITIONS.get(old_state, [])
        if new_state not in allowed:
            raise ValueError(f"FR-EC-401 Violation: Invalid transition from {old_state.value} to {new_state.value}.")

        # Rule: No experiment may reach SCHEDULED without an attached, falsifiable Hypothesis
        if new_state == ExperimentState.SCHEDULED:
            if not exp.hypothesis_id or exp.hypothesis_id == "none":
                if not hypothesis:
                    raise ValueError("FR-EC-401 Violation: SCHEDULED state requires an attached Hypothesis.")
            if hypothesis and hypothesis.status not in [HypothesisStatus.ACTIVE, HypothesisStatus.PROPOSED]:
                raise ValueError("FR-EC-401 Violation: Attached Hypothesis is not valid/active.")

        exp.state = new_state
        exp.timeline.append({
            "from_state": old_state.value,
            "to_state": new_state.value,
            "correlation_id": correlation_id
        })

        if self.broker:
            env = EventEnvelope(
                event_type="ExperimentStateChanged",
                correlation_id=correlation_id,
                producer="ExperimentEngine",
                payload={"experiment_id": exp.id, "old_state": old_state.value, "new_state": new_state.value}
            )
            self.broker.publish("core.events", env)

        return exp

    def issue_directive(
        self,
        exp_id: str,
        content_spec: Dict,
        measurement_plan: Dict,
        correlation_id: str = "none"
    ) -> ExperimentDirective:
        """FR-EC-402: Issue ExperimentDirective to execution layer."""
        exp = self.get_experiment(exp_id)
        if not exp or exp.state not in [ExperimentState.SCHEDULED, ExperimentState.APPROVED]:
            raise ValueError(f"Experiment {exp_id} must be SCHEDULED or APPROVED to issue directive.")

        directive = ExperimentDirective(
            experiment_id=exp.id,
            content_spec=content_spec,
            measurement_plan=measurement_plan
        )
        exp.directive = directive

        # Emit ExperimentDirectiveIssued event
        event = ExperimentDirectiveIssued(
            experiment_id=exp.id,
            genome_version="0.1.0",
            target_scope={"platform": content_spec.get("platform", "generic")},
            parameters=content_spec
        )
        if self.broker:
            env = event.wrap(producer="ExperimentEngine", correlation_id=correlation_id)
            self.broker.publish("core.events", env)

        return directive
