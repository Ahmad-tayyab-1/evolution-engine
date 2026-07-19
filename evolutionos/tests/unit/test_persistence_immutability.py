"""
Unit tests verifying append-only event store (INF-DB-001) and knowledge immutability (ADR-004).
"""
import pytest
from sqlalchemy.orm import sessionmaker
from evolutionos.infrastructure.persistence.database import get_engine, init_db
from evolutionos.infrastructure.persistence.models import CoreEventStoreModel, KnowledgeRecordModel


@pytest.fixture
def db_session():
    """Create a temporary in-memory SQLite database for test isolation."""
    engine = get_engine("sqlite:///:memory:")
    init_db(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def test_core_event_store_append_only(db_session):
    """INF-DB-001: Verify event store rows can be added, but raise errors on update or delete attempts."""
    event = CoreEventStoreModel(
        event_id="evt_001",
        event_type="ObservationIntegrated",
        occurred_at="2026-07-18T12:00:00Z",
        correlation_id="corr_100",
        producer="ObservationGateway",
        payload_json='{"ctr": 0.12}'
    )
    db_session.add(event)
    db_session.commit()

    # Verify read
    saved = db_session.query(CoreEventStoreModel).filter_by(event_id="evt_001").first()
    assert saved is not None
    assert saved.correlation_id == "corr_100"

    # Attempt illegal update
    saved.producer = "MaliciousActor"
    with pytest.raises(RuntimeError, match="INF-DB-001 Violation.*IMMUTABLE"):
        db_session.commit()
    db_session.rollback()

    # Attempt illegal delete
    saved = db_session.query(CoreEventStoreModel).filter_by(event_id="evt_001").first()
    db_session.delete(saved)
    with pytest.raises(RuntimeError, match="INF-DB-001 Violation.*cannot be deleted"):
        db_session.commit()
    db_session.rollback()


def test_knowledge_record_immutability(db_session):
    """ADR-004: Verify KnowledgeRecord allows status updates (`CANDIDATE -> ACTIVE`), but forbids statement/confidence mutation."""
    kr = KnowledgeRecordModel(
        id="kr_101",
        scope_json='{"niche": "science"}',
        status="CANDIDATE",
        rule_statement="Short intros increase retention",
        confidence=0.75
    )
    db_session.add(kr)
    db_session.commit()

    # Legal status transition
    kr.status = "ACTIVE"
    db_session.commit()  # Should pass without errors
    assert kr.status == "ACTIVE"

    # Illegal mutation of rule_statement or confidence
    kr.confidence = 0.99
    with pytest.raises(RuntimeError, match="ADR-004 Violation.*IMMUTABLE"):
        db_session.commit()
    db_session.rollback()
