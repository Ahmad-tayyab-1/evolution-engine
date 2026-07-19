"""
Fitness Timeline Projection (`Plan.md` Appendix B / Section 18.2).
Read-only CQRS projection building multi-dimensional fitness evolution trajectory over time.
"""
from typing import Dict, Any, List, Optional
from evolutionos.core.events.catalog import EventEnvelope
from evolutionos.infrastructure.messaging.broker import MessageBroker


class FitnessTimelineProjection:
    def __init__(self, broker: Optional[MessageBroker] = None):
        self.broker = broker
        self.timeline: List[Dict[str, Any]] = []
        if self.broker:
            self.broker.subscribe("core.events", "fitness_timeline", "fitness_timeline_builder", self._on_event)

    def _on_event(self, envelope: EventEnvelope) -> None:
        if envelope.event_type == "FitnessComputed":
            payload = envelope.payload
            self.timeline.append({
                "experiment_id": payload.get("experiment_id", ""),
                "scalar_score": payload.get("vector", {}).get("scalar_score", 0.0),
                "learning_yield": payload.get("vector", {}).get("learning_yield", 0.0),
                "computed_at": envelope.occurred_at
            })

    def get_timeline(self, limit: int = 50) -> List[Dict[str, Any]]:
        return self.timeline[-limit:]
