"""
Persistence Models and Event Store Schema (INF-DB-001, ADR-014).

Defines `core_events` table with DB-level append-only enforcement (raises errors on UPDATE/DELETE attempts),
plus read/workflow schemas (`core_read`, `knowledge_table`, `workflow_state`).
"""
from datetime import datetime, timezone
import json
from sqlalchemy import (
    Column, String, Integer, Float, DateTime, Text, Boolean, event
)
from evolutionos.infrastructure.persistence.database import Base


class CoreEventStoreModel(Base):
    """INF-DB-001 & ADR-011: Canonical append-only event store table."""
    __tablename__ = "core_events"

    sequence_id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(String(64), unique=True, nullable=False, index=True)
    event_type = Column(String(100), nullable=False, index=True)
    occurred_at = Column(String(64), nullable=False)
    correlation_id = Column(String(64), nullable=False, index=True)
    causation_id = Column(String(64), nullable=True)
    producer = Column(String(100), nullable=False)
    schema_version = Column(String(20), default="0.1.0")
    payload_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def set_payload(self, data: dict) -> None:
        self.payload_json = json.dumps(data)

    def get_payload(self) -> dict:
        return json.loads(self.payload_json) if self.payload_json else {}


# INF-DB-001: Append-Only DB-Level Enforcement via SQLAlchemy Event Listeners
# Prevent any modification or deletion of recorded event store rows.

@event.listens_for(CoreEventStoreModel, "before_update")
def prevent_event_update(mapper, connection, target):
    raise RuntimeError(
        f"INF-DB-001 Violation: CoreEventStoreModel rows are append-only and IMMUTABLE. Attempted update on sequence_id={target.sequence_id}"
    )


@event.listens_for(CoreEventStoreModel, "before_delete")
def prevent_event_delete(mapper, connection, target):
    raise RuntimeError(
        f"INF-DB-001 Violation: CoreEventStoreModel rows cannot be deleted. Attempted delete on sequence_id={target.sequence_id}"
    )


class KnowledgeRecordModel(Base):
    """SQL storage table for KnowledgeRecords (ADR-004 immutable rows)."""
    __tablename__ = "knowledge_records"

    id = Column(String(64), primary_key=True)
    scope_json = Column(Text, nullable=False)  # JSON representation of scope
    hypothesis_id = Column(String(64), nullable=True)
    status = Column(String(30), default="CANDIDATE", index=True)
    # CANDIDATE | ACTIVE | SUPERSEDED | DEPRECATED | ARCHIVED
    rule_statement = Column(Text, nullable=False)
    confidence = Column(Float, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    supersedes_id = Column(String(64), nullable=True)
    superseded_by_id = Column(String(64), nullable=True)


@event.listens_for(KnowledgeRecordModel, "before_update")
def enforce_knowledge_immutability(mapper, connection, target):
    """ADR-004: Only status transition fields and supersession links may be updated."""
    # SQLAlchemy target tracks modified attributes
    state = target._sa_instance_state
    modified = [attr.key for attr in state.attrs if attr.history.has_changes()]
    allowed_mutations = {"status", "superseded_by_id"}
    illegal = set(modified) - allowed_mutations
    if illegal:
        raise RuntimeError(
            f"ADR-004 Violation: KnowledgeRecordModel fields {illegal} are IMMUTABLE. Only status and superseded_by_id may transition."
        )


class BeliefSnapshotModel(Base):
    """Fast read projection for active beliefs (Reasoning hot path)."""
    __tablename__ = "belief_snapshots"

    id = Column(String(64), primary_key=True)
    statement = Column(Text, nullable=False)
    confidence = Column(Float, nullable=False)
    stability = Column(Float, default=1.0)
    scope_json = Column(Text, nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class SagaCheckpointModel(Base):
    """Persistence model for EvolutionCycleSaga checkpointing (FR-EC-502)."""
    __tablename__ = "saga_checkpoints"

    cycle_id = Column(String(64), primary_key=True)
    current_step = Column(String(50), nullable=False)
    state_json = Column(Text, nullable=False)
    status = Column(String(30), default="RUNNING")  # RUNNING | COMPLETED | FAILED | ABORTED
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
