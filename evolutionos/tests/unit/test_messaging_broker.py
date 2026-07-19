"""
Unit tests for Event Catalog and Messaging Brokers (EC-EVT-002, ADR-009).
"""
import pytest
from evolutionos.core.events.catalog import (
    EventEnvelope, ObservationIntegrated, LessonExtracted, KnowledgeActivated, BeliefRevised
)
from evolutionos.infrastructure.messaging.redis_streams import MemoryBroker


def test_event_envelope_serialization():
    """Verify EventEnvelope wraps domain events and serializes correctly per EC-EVT-002."""
    obs_event = ObservationIntegrated(
        observation_id="obs_123",
        feedback_level=2,
        scope={"niche": "science", "format": "long"},
        metrics={"ctr": 0.08, "retention": 0.65}
    )
    envelope = obs_event.wrap(producer="ObservationGateway", correlation_id="cycle_999")

    assert envelope.event_type == "ObservationIntegrated"
    assert envelope.correlation_id == "cycle_999"
    assert envelope.producer == "ObservationGateway"
    assert envelope.payload["observation_id"] == "obs_123"
    assert envelope.payload["metrics"]["ctr"] == 0.08

    # Test round trip to dict / json
    data = envelope.to_dict()
    reconstructed = EventEnvelope.from_dict(data)
    assert reconstructed.event_id == envelope.event_id
    assert reconstructed.payload == envelope.payload


def test_memory_broker_pub_sub_and_ack():
    """Verify MemoryBroker pub/sub dispatch and stream reading."""
    broker = MemoryBroker()
    received_events = []

    def callback(env: EventEnvelope):
        received_events.append(env)

    broker.subscribe("core.events", "test_group", "consumer_1", callback)

    lesson = LessonExtracted(
        lesson_id="less_001",
        knowledge_record_id="kr_456",
        rule_statement="Question hooks increase CTR by 15%",
        confidence=0.88,
        p_value=0.02
    )
    env = lesson.wrap(producer="LearningEngine", correlation_id="cycle_101")
    msg_id = broker.publish("core.events", env)

    assert len(received_events) == 1
    assert received_events[0].payload["lesson_id"] == "less_001"
    assert msg_id == "1-0"

    # Test reading from stream
    history = broker.read_stream("core.events", count=5)
    assert len(history) == 1
    assert history[0].correlation_id == "cycle_101"

    # Test acknowledge
    assert broker.acknowledge("core.events", "test_group", msg_id) is True
