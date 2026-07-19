"""
Event Store (`Plan.md` Appendix B / Volume 4).
Canonical persistence interface and repository for append-only domain event history (`ADR-004`).
"""
from evolutionos.infrastructure.persistence.models import EventStore

__all__ = ["EventStore"]
