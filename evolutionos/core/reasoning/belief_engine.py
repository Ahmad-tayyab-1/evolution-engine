"""
Belief Engine (FR-EC-201, FR-EC-202, FR-EC-203, ADR-007).

Manages Belief lifecycle, Bayesian-inspired confidence updates, recency weighting,
and confidence decay toward 0.5 over unvalidated windows (`decay_window = 90 days`).
"""
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional
from evolutionos.core.domain.ontology import Belief, BeliefStatus, ConfidencePoint, Scope
from evolutionos.core.events.catalog import BeliefUpdated, EventEnvelope
from evolutionos.infrastructure.messaging.broker import MessageBroker
from evolutionos.config.settings import settings


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class BeliefEngine:
    """Manages confidence updates, stability scores, and decay across Beliefs."""

    def __init__(self, broker: Optional[MessageBroker] = None):
        self.beliefs: Dict[str, Belief] = {}
        self.broker = broker

    def add_belief(self, belief: Belief) -> str:
        self.beliefs[belief.id] = belief
        return belief.id

    def get_belief(self, belief_id: str) -> Optional[Belief]:
        return self.beliefs.get(belief_id)

    def update_confidence(
        self,
        belief_id: str,
        direction: int,
        evidence_weight: float = 0.10,
        trigger: str = "EVIDENCE_OBSERVED",
        causing_event_id: str = "unknown",
        correlation_id: str = "none"
    ) -> Belief:
        """FR-EC-202: Bayesian-inspired confidence update bounded in (0.01, 0.99)."""
        belief = self.get_belief(belief_id)
        if not belief:
            raise ValueError(f"Belief {belief_id} not found.")

        # posterior = prior + learning_rate * (evidence_weight * direction - prior_pull)
        # prior_pull pulls unvalidated priors toward 0.5
        prior = belief.confidence
        prior_pull = 0.02 * (prior - 0.5)
        learning_rate = 0.20

        posterior = prior + learning_rate * (evidence_weight * direction - prior_pull)
        # Bounded between 0.01 and 0.99 (CON-ETH-003)
        posterior = max(0.01, min(0.99, posterior))

        # Track history
        belief.confidence_history.append(
            ConfidencePoint(
                timestamp=utc_now().isoformat(),
                confidence=posterior,
                trigger=trigger,
                causing_event_id=causing_event_id
            )
        )
        belief.confidence = posterior
        belief.last_challenged_at = utc_now().isoformat()
        if direction > 0:
            belief.last_validated_at = utc_now().isoformat()

        # Update stability score based on history variance
        if len(belief.confidence_history) >= 3:
            conf_vals = [cp.confidence for cp in belief.confidence_history[-5:]]
            mean_conf = sum(conf_vals) / len(conf_vals)
            variance = sum((c - mean_conf) ** 2 for c in conf_vals) / len(conf_vals)
            # Higher variance -> lower stability
            belief.stability_score = max(0.0, min(1.0, 1.0 - variance * 10))

        # Emit BeliefUpdated / ConfidenceUpdated event
        event = BeliefUpdated(
            belief_id=belief.id,
            old_confidence=prior,
            new_confidence=posterior,
            reason=trigger
        )
        if self.broker:
            env = event.wrap(producer="BeliefEngine", correlation_id=correlation_id)
            self.broker.publish("core.events", env)

        return belief

    def apply_decay(self, correlation_id: str = "decay_cycle") -> List[str]:
        """FR-EC-203: Decay unvalidated beliefs (> decay_window) toward 0.5."""
        stale_events = []
        now = utc_now()
        decay_days = settings.belief_decay_days

        for belief in self.beliefs.values():
            if belief.status != BeliefStatus.ACTIVE:
                continue

            last_valid_str = belief.last_validated_at or belief.confidence_history[0].timestamp if belief.confidence_history else None
            if not last_valid_str:
                continue

            try:
                # Handle ISO timestamps with Z or offset
                clean_str = last_valid_str.replace("Z", "+00:00")
                last_valid = datetime.fromisoformat(clean_str)
                if last_valid.tzinfo is None:
                    last_valid = last_valid.replace(tzinfo=timezone.utc)
            except Exception:
                continue

            if (now - last_valid) > timedelta(days=decay_days):
                # Decay toward 0.5 by 5%
                old_conf = belief.confidence
                if belief.confidence > 0.5:
                    belief.confidence = max(0.5, belief.confidence - 0.05)
                elif belief.confidence < 0.5:
                    belief.confidence = min(0.5, belief.confidence + 0.05)

                stale_events.append(belief.id)
                if self.broker:
                    env = EventEnvelope(
                        event_type="BeliefStale",
                        correlation_id=correlation_id,
                        producer="BeliefEngine",
                        payload={"belief_id": belief.id, "old_confidence": old_conf, "new_confidence": belief.confidence}
                    )
                    self.broker.publish("core.events", env)

        return stale_events
