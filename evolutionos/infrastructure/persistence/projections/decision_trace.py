"""
Decision Trace Projection (`Plan.md` Appendix B / Section 18.2).
Read-only CQRS projection building chronological decision history trace.
"""
from evolutionos.dashboard.api.projections import DecisionTraceProjection

__all__ = ["DecisionTraceProjection"]
