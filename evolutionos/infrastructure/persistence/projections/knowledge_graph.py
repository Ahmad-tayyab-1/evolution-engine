"""
Knowledge Graph Projection (`Plan.md` Section 18.2, Developer Handbook Section 10).

Read-only projection that subscribes to domain events (`KnowledgeRecordCreated`,
`KnowledgeRecordConsolidated`, `BeliefUpdated`) and builds a queryable graph structure
of records, rules, and causal edges without querying the transactional event store.
"""
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from evolutionos.core.events.catalog import EventEnvelope
from evolutionos.infrastructure.messaging.broker import MessageBroker

logger = logging.getLogger("evolutionos.infrastructure.projections.knowledge_graph")


class GraphNode(BaseModel):
    node_id: str
    node_type: str  # "RECORD", "RULE", "BELIEF", "LESSON"
    statement: str
    confidence: float
    status: str
    updated_at: str


class GraphEdge(BaseModel):
    source_id: str
    target_id: str
    relation: str   # "CONTRADICTS", "SUPPORTS", "DERIVED_FROM", "SUPERSEDES"
    weight: float = 1.0


class KnowledgeGraphProjection:
    """Read-only CQRS projection for Knowledge Graph visualization and traversal (`Section 18.2`)."""

    def __init__(self, broker: Optional[MessageBroker] = None):
        self.broker = broker
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: List[GraphEdge] = []

        if self.broker:
            self._subscribe()

    def _subscribe(self) -> None:
        self.broker.subscribe("core.events", "graph_projection", "knowledge_graph_builder", self._on_event)

    def _on_event(self, envelope: EventEnvelope) -> None:
        etype = envelope.event_type
        payload = envelope.payload

        if etype in ["KnowledgeRecordCreated", "KnowledgeRecordConsolidated"]:
            node_id = payload.get("record_id", f"kr_{envelope.correlation_id}")
            self.nodes[node_id] = GraphNode(
                node_id=node_id,
                node_type=payload.get("type", "RECORD"),
                statement=payload.get("statement", ""),
                confidence=payload.get("confidence", 0.5),
                status=payload.get("status", "ACTIVE"),
                updated_at=envelope.occurred_at
            )
            # Add provenance edges if causal parent present
            parent_id = payload.get("parent_id")
            if parent_id:
                self.edges.append(GraphEdge(
                    source_id=parent_id,
                    target_id=node_id,
                    relation="DERIVED_FROM",
                    weight=payload.get("confidence", 0.5)
                ))

        elif etype == "BeliefUpdated":
            b_id = payload.get("belief_id", f"b_{envelope.correlation_id}")
            self.nodes[b_id] = GraphNode(
                node_id=b_id,
                node_type="BELIEF",
                statement=f"Belief {b_id}",
                confidence=payload.get("confidence", 0.5),
                status="ACTIVE",
                updated_at=envelope.occurred_at
            )

    def get_node(self, node_id: str) -> Optional[GraphNode]:
        return self.nodes.get(node_id)

    def get_subgraph(self, root_id: str, max_depth: int = 2) -> Dict[str, Any]:
        """Traverse graph starting from root_id up to max_depth."""
        visited_nodes = set()
        visited_edges = []
        queue = [(root_id, 0)]

        while queue:
            curr_id, depth = queue.pop(0)
            if curr_id in visited_nodes or depth > max_depth:
                continue
            visited_nodes.add(curr_id)

            for edge in self.edges:
                if edge.source_id == curr_id and edge.target_id not in visited_nodes:
                    visited_edges.append(edge)
                    queue.append((edge.target_id, depth + 1))
                elif edge.target_id == curr_id and edge.source_id not in visited_nodes:
                    visited_edges.append(edge)
                    queue.append((edge.source_id, depth + 1))

        nodes_out = [self.nodes[nid].model_dump() for nid in visited_nodes if nid in self.nodes]
        edges_out = [e.model_dump() for e in visited_edges]
        return {"nodes": nodes_out, "edges": edges_out}
