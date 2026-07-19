"""
EventBus Port Interface (`Plan.md` Section 5 / Appendix B).
Abstract boundary contract defining pub/sub and event emission interface required by Core without external messaging imports.
"""
from abc import ABC, abstractmethod
from typing import Callable, Any
from evolutionos.core.events.catalog import EventEnvelope


class EventBus(ABC):
    @abstractmethod
    def publish(self, topic: str, envelope: EventEnvelope) -> str:
        pass

    @abstractmethod
    def subscribe(self, topic: str, consumer_group: str, consumer_name: str, callback: Callable[[EventEnvelope], None]) -> None:
        pass
