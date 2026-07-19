"""
Unit tests for Knowledge Graph Projection and Versioned Prompts (`Plan.md` Section 16 & Section 18.2).
"""
import pytest
from evolutionos.core.events.catalog import EventEnvelope
from evolutionos.infrastructure.messaging.redis_streams import MemoryBroker
from evolutionos.infrastructure.persistence.projections.knowledge_graph import KnowledgeGraphProjection
from evolutionos.execution.prompts.registry.lesson_extraction_v1 import render_prompt, LessonExtractionPromptMetadata


def test_knowledge_graph_projection_subscribes_and_builds_graph():
    broker = MemoryBroker()
    projection = KnowledgeGraphProjection(broker=broker)

    # Emit domain events
    created_env = EventEnvelope(
        event_type="KnowledgeRecordCreated",
        producer="KnowledgeEngine",
        correlation_id="corr_123",
        payload={
            "record_id": "kr_001",
            "type": "LESSON",
            "statement": "Increasing CTR boosts watch hours",
            "confidence": 0.85,
            "status": "ACTIVE",
            "parent_id": "kr_root"
        }
    )
    broker.publish("core.events", created_env)

    belief_env = EventEnvelope(
        event_type="BeliefUpdated",
        producer="BeliefEngine",
        correlation_id="corr_123",
        payload={
            "belief_id": "b_001",
            "confidence": 0.90
        }
    )
    broker.publish("core.events", belief_env)

    # Verify nodes and edges created
    assert "kr_001" in projection.nodes
    assert projection.nodes["kr_001"].confidence == 0.85
    assert "b_001" in projection.nodes
    assert len(projection.edges) == 1
    assert projection.edges[0].source_id == "kr_root"
    assert projection.edges[0].target_id == "kr_001"

    # Verify subgraph traversal
    subgraph = projection.get_subgraph("kr_root", max_depth=2)
    assert len(subgraph["nodes"]) == 1
    assert len(subgraph["edges"]) == 1


def test_lesson_extraction_v1_render_and_metadata():
    meta = LessonExtractionPromptMetadata()
    assert meta.prompt_id == "lesson_extraction_v1"
    assert meta.version == "1.0.0"

    rendered = render_prompt(
        experiment_id="exp_999",
        hypothesis_statement="IF ctr increases THEN views increase",
        performance_delta=0.12,
        surprise_score=0.45,
        observations_summary="Views jumped by 1500"
    )
    assert "exp_999" in rendered
    assert "IF ctr increases THEN views increase" in rendered
    assert "lessons" in rendered
