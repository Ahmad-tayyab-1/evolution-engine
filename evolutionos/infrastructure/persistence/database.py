"""
Universal Database Engine (ADR-014, INF-DB-001).

Configures SQLAlchemy session management supporting PostgreSQL (`pgvector`) with SQLite fallback (`v0.1`/`v0.2`).
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from evolutionos.config.settings import settings

Base = declarative_base()


def get_engine(url: str = None):
    """Return SQLAlchemy database engine."""
    db_url = url or settings.db_url
    # For SQLite we add check_same_thread=False
    if db_url.startswith("sqlite"):
        return create_engine(db_url, connect_args={"check_same_thread": False}, future=True)
    return create_engine(db_url, future=True)


engine = get_engine()
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, future=True)


def init_db(engine_instance=None):
    """Initialize database schemas and tables."""
    target_engine = engine_instance or engine
    Base.metadata.create_all(bind=target_engine)


def get_db():
    """Generator providing session context."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
