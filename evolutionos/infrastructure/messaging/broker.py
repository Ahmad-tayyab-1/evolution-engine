"""
MessageBroker Interface (ADR-009, ADR-015).

Abstract port defining asynchronous pub/sub and stream handling across bounded contexts.
"""
from abc import ABC, abstractmethod
from typing import Callable, Optional
from evolutionos.core.events.catalog import EventEnvelope


class MessageBroker(ABC):
    """Abstract port for asynchronous event broker."""

    @abstractmethod
    def publish(self, stream_or_topic: str, event: EventEnvelope) -> str:
        """Publish an EventEnvelope to a stream/topic and return message ID."""
        pass

    @abstractmethod
    def subscribe(self, stream_or_topic: str, consumer_group: str, consumer_name: str, callback: Callable[[EventEnvelope], None]) -> None:
        """Subscribe a consumer callback to a stream/topic."""
        pass

    @abstractmethod
    def read_stream(self, stream_or_topic: str, count: int = 10, start_id: str = "0-0") -> list[EventEnvelope]:
        """Read up to `count` events from a stream starting from `start_id`."""
        pass

    @abstractmethod
    def acknowledge(self, stream_or_topic: str, consumer_group: str, message_id: str) -> bool:
        """Acknowledge processing of a message."""
        pass
