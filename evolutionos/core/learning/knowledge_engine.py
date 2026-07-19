"""
Knowledge Engine (FR-EC-101 through FR-EC-104, ADR-004).

Manages KnowledgeRecord CRUD, vector similarity / semantic search, graph edge management,
and consolidation of records exceeding similarity thresholds. Enforces append-only immutability.
"""
import math
from typing import Any, Dict, List, Optional, Tuple
from evolutionos.core.domain.ontology import (
    KnowledgeRecord, KnowledgeStatus, KnowledgeType, KnowledgeEdge, KnowledgeRelation, Scope
)
from evolutionos.config.settings import settings


class KnowledgeEngine:
    """Manages immutable knowledge store, semantic similarity, and graph relationships."""

    def __init__(self):
        self.records: Dict[str, KnowledgeRecord] = {}
        self.edges: Dict[str, KnowledgeEdge] = {}

    def add_record(self, record: KnowledgeRecord) -> str:
        """FR-EC-101 & ADR-004: Add new immutable knowledge record."""
        if record.id in self.records:
            raise RuntimeError(f"ADR-004 Violation: KnowledgeRecord {record.id} already exists.")
        self.records[record.id] = record
        return record.id

    def get_record(self, record_id: str) -> Optional[KnowledgeRecord]:
        return self.records.get(record_id)

    def add_edge(self, edge: KnowledgeEdge) -> str:
        self.edges[edge.id] = edge
        return edge.id

    def transition_status(self, record_id: str, new_status: KnowledgeStatus, superseded_by: Optional[str] = None) -> KnowledgeRecord:
        """FR-EC-102: Transition status. Modifies only status / supersession fields per ADR-004."""
        record = self.get_record(record_id)
        if not record:
            raise ValueError(f"KnowledgeRecord {record_id} not found.")
        record.status = new_status
        if superseded_by:
            record.superseded_by_id = superseded_by
        return record

    def query_by_scope(self, scope: Scope, min_confidence: float = 0.0) -> List[KnowledgeRecord]:
        """FR-EC-103: Query active records matching scope and confidence threshold."""
        results = []
        for r in self.records.values():
            if r.status in [KnowledgeStatus.ACTIVE, KnowledgeStatus.CANDIDATE]:
                if r.confidence >= min_confidence and r.scope.is_compatible_with(scope):
                    results.append(r)
        return results

    def query_related(self, record_id: str, depth: int = 1) -> List[KnowledgeRecord]:
        """FR-EC-103: Graph traversal finding related records up to `depth`."""
        visited = set([record_id])
        current_layer = set([record_id])
        related_records = []

        for _ in range(depth):
            next_layer = set()
            for edge in self.edges.values():
                if edge.from_id in current_layer and edge.to_id not in visited:
                    visited.add(edge.to_id)
                    next_layer.add(edge.to_id)
                    if edge.to_id in self.records:
                        related_records.append(self.records[edge.to_id])
                elif edge.to_id in current_layer and edge.from_id not in visited:
                    visited.add(edge.from_id)
                    next_layer.add(edge.from_id)
                    if edge.from_id in self.records:
                        related_records.append(self.records[edge.from_id])
            current_layer = next_layer
        return related_records

    def compute_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Compute cosine similarity between embedding vectors."""
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0
        dot = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

    def consolidate(self, similarity_threshold: Optional[float] = None) -> List[Tuple[str, str, str]]:
        """FR-EC-104: Consolidate records exceeding similarity threshold. Returns list of (consolidated_id, r1_id, r2_id)."""
        threshold = similarity_threshold or settings.consolidation_similarity_threshold
        active_ids = [r.id for r in self.records.values() if r.status == KnowledgeStatus.ACTIVE and r.embedding_vector]
        consolidated_events = []

        for i in range(len(active_ids)):
            for j in range(i + 1, len(active_ids)):
                id1, id2 = active_ids[i], active_ids[j]
                r1, r2 = self.records[id1], self.records[id2]
                if r1.status != KnowledgeStatus.ACTIVE or r2.status != KnowledgeStatus.ACTIVE:
                    continue
                sim = self.compute_similarity(r1.embedding_vector, r2.embedding_vector)
                if sim >= threshold:
                    # Create consolidated record
                    merged_statement = f"Consolidated ({r1.type.value}): {r1.statement} | {r2.statement}"
                    merged_conf = max(r1.confidence, r2.confidence)
                    cons_record = KnowledgeRecord(
                        type=r1.type,
                        statement=merged_statement,
                        scope=r1.scope,
                        confidence=merged_conf,
                        confidence_basis="INHERITED",
                        evidence_refs=list(set(r1.evidence_refs + r2.evidence_refs + [id1, id2])),
                        provenance=r1.provenance,
                        status=KnowledgeStatus.ACTIVE,
                        embedding_vector=r1.embedding_vector
                    )
                    self.add_record(cons_record)
                    # Mark originals ARCHIVED per FR-EC-104
                    self.transition_status(id1, KnowledgeStatus.ARCHIVED, superseded_by=cons_record.id)
                    self.transition_status(id2, KnowledgeStatus.ARCHIVED, superseded_by=cons_record.id)
                    consolidated_events.append((cons_record.id, id1, id2))
        return consolidated_events
