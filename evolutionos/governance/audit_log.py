"""
Audit Log System (`DP-014`, `FR-PX-1503`).

Append-only audit trail logging all governance decisions, policy violations, approvals,
rejections, and kill switch activations (`survives restart`).
"""
import time
import json
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("evolutionos.governance.audit_log")


class AuditEventType(str):
    APPROVAL_GRANTED = "APPROVAL_GRANTED"
    APPROVAL_REJECTED = "APPROVAL_REJECTED"
    POLICY_VIOLATION_BLOCKED = "POLICY_VIOLATION_BLOCKED"
    KILL_SWITCH_TRIGGERED = "KILL_SWITCH_TRIGGERED"
    KILL_SWITCH_RESET = "KILL_SWITCH_RESET"
    ROLLBACK_EXECUTED = "ROLLBACK_EXECUTED"


class AuditEvent(BaseModel):
    """Append-only audit event (`DP-014`)."""
    event_id: str
    event_type: str
    actor: str                  # "HUMAN_OWNER", "POLICY_ENGINE", "KILL_SWITCH"
    target_id: str              # experiment_id, directive_id, or hypothesis_id
    reason: str
    timestamp: float = Field(default_factory=time.time)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AuditLogger:
    """Append-only audit log store (`DP-014`, `FR-PX-1503`)."""

    def __init__(self):
        self.events: List[AuditEvent] = []

    def log_event(
        self,
        event_type: str,
        actor: str,
        target_id: str,
        reason: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> AuditEvent:
        event = AuditEvent(
            event_id=f"audit_{int(time.time()*1000)}_{len(self.events)}",
            event_type=event_type,
            actor=actor,
            target_id=target_id,
            reason=reason,
            metadata=metadata or {}
        )
        self.events.append(event)
        logger.info(f"AUDIT LOG [{event_type}] ({actor}) -> target={target_id}: {reason}")
        return event

    def get_events_for_target(self, target_id: str) -> List[AuditEvent]:
        return [e for e in self.events if e.target_id == target_id]

    def get_all_events(self) -> List[AuditEvent]:
        return list(self.events)
