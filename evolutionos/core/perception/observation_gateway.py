"""
Observation Gateway (FR-EC-301, FR-EC-302).

Ingests raw or normalized observations from execution layers, validates schemas,
quarantines impossible/malformed data without silent drops, and emits `ObservationIntegrated`.
"""
import logging
from typing import Any, Dict, List, Optional, Tuple
from evolutionos.core.domain.ontology import Observation, ObservationStatus, ObservationQuality
from evolutionos.core.events.catalog import ObservationIntegrated, DomainEvent
from evolutionos.infrastructure.messaging.broker import MessageBroker

logger = logging.getLogger("evolutionos.perception.gateway")


class ObservationGateway:
    """Ingests and validates observations before integrating into Evolution Core."""

    def __init__(self, broker: Optional[MessageBroker] = None, known_experiments: Optional[set] = None):
        self.broker = broker
        self.known_experiments = known_experiments or set()
        self.quarantine_log: List[Dict[str, Any]] = []
        self.integrated_log: List[Observation] = []

    def register_experiment(self, experiment_id: str) -> None:
        """Register known experiment ID for validation."""
        self.known_experiments.add(experiment_id)

    def process_observation(
        self,
        raw_data: Dict[str, Any],
        correlation_id: str,
        producer: str = "ObservationGateway"
    ) -> Tuple[Optional[Observation], Optional[str]]:
        """Validate, quarantine or integrate observation. Returns (Observation, quarantine_reason)."""
        # 1. Schema Check
        try:
            obs = Observation.model_validate(raw_data)
        except Exception as e:
            reason = f"Schema validation failed: {e}"
            self._quarantine(raw_data.get("id", "unknown"), reason, raw_data, correlation_id)
            return None, reason

        # 2. Unknown Experiment Check (if strict known list is non-empty)
        if self.known_experiments and obs.experiment_id not in self.known_experiments:
            reason = f"Unknown experiment_id: {obs.experiment_id}"
            obs.status = ObservationStatus.QUARANTINED
            self._quarantine(obs.id, reason, obs.model_dump(), correlation_id)
            return obs, reason

        # 3. Impossible Value Check (e.g. CTR or rate > 1.0 or < 0.0 when unit is percentage/ratio)
        reason = self._check_impossible_values(obs)
        if reason:
            obs.status = ObservationStatus.QUARANTINED
            self._quarantine(obs.id, reason, obs.model_dump(), correlation_id)
            return obs, reason

        # 4. Integrate successfully
        obs.status = ObservationStatus.INTEGRATED
        self.integrated_log.append(obs)

        # Emit ObservationIntegrated event
        event = ObservationIntegrated(
            observation_id=obs.id,
            feedback_level=1,  # Default level; SignalClassifier updates/routes
            scope={"platform": obs.platform},
            metrics={obs.metric: float(obs.value) if isinstance(obs.value, (int, float)) else 0.0}
        )
        if self.broker:
            env = event.wrap(producer=producer, correlation_id=correlation_id)
            self.broker.publish("core.events", env)

        return obs, None

    def _check_impossible_values(self, obs: Observation) -> Optional[str]:
        val = obs.value
        if isinstance(val, (int, float)):
            metric_lower = obs.metric.lower()
            if any(term in metric_lower for term in ["rate", "ctr", "ratio", "percent"]):
                # If metric claims to be a rate or ratio, check standard bounds [0, 1.0] or [0, 100]
                if obs.unit in ["%", "percent"]:
                    if not (0.0 <= val <= 100.0):
                        return f"Impossible percentage value {val} for metric {obs.metric}"
                else:
                    # Normalized rate [0.0, 1.0]
                    if not (0.0 <= val <= 1.0) and val > 1.0:
                        return f"Impossible normalized rate {val} for metric {obs.metric} (expected 0.0-1.0)"
            if val < 0 and "growth" not in metric_lower and "delta" not in metric_lower:
                return f"Negative value {val} not permitted for metric {obs.metric}"
        return None

    def _quarantine(self, obs_id: str, reason: str, raw: Dict[str, Any], correlation_id: str) -> None:
        logger.warning(f"Quarantining observation {obs_id}: {reason}")
        self.quarantine_log.append({
            "observation_id": obs_id,
            "reason": reason,
            "raw_data": raw,
            "correlation_id": correlation_id
        })
