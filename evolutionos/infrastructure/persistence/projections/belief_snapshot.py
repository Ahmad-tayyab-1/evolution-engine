"""
Belief Snapshot Projection (`Plan.md` Appendix B / Section 18.2).
Read-only CQRS projection maintaining current confidence snapshot across all domain beliefs.
"""
from evolutionos.dashboard.api.projections import BeliefSnapshotProjection

__all__ = ["BeliefSnapshotProjection"]
