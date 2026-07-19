"""
Dashboard FastAPI REST API (`Section 18.1`, `Section 18.2`, `FR-PX-1601`).

Exposes read-only endpoints against `CQRSProjectionEngine` views (`Evolution Overview`,
`Experiment Board`, `Decision Trace`, `Knowledge Browser`, `Belief Inspector`, `Pipeline Monitor`,
`Cost Center`, `System Health`, and `Approval Inbox`).
Also provides governance action endpoints (`approve`, `reject`, `kill-switch`).
"""
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status
from evolutionos.dashboard.api.projections import CQRSProjectionEngine
from evolutionos.governance.kill_switch import KillSwitch
from evolutionos.governance.audit_log import AuditLogger, AuditEventType
from evolutionos.infrastructure.messaging.redis_streams import MemoryBroker

logger = logging.getLogger("evolutionos.dashboard.api.main")

# Global instances for API
broker = MemoryBroker()
projections = CQRSProjectionEngine(broker=broker)
kill_switch = KillSwitch.get_instance()
audit_logger = AuditLogger()

app = FastAPI(
    title="EvolutionOS Dashboard & Governance API",
    description="Read-only projections (Section 18) + Supervised Autonomy (Section 17)",
    version="1.0.0"
)


class ApprovalActionRequest(BaseModel):
    actor: str = "HUMAN_OWNER"
    reason: str = "Approved via dashboard"


class KillSwitchRequest(BaseModel):
    action: str  # "TRIGGER" or "RESET"
    reason: str = "Emergency trigger via dashboard"
    authorization_code: Optional[str] = None


@app.get("/api/v1/overview", response_model=Dict[str, Any])
def get_overview():
    """Section 18.1: Evolution Overview view."""
    return projections.get_overview()


@app.get("/api/v1/experiments", response_model=List[Dict[str, Any]])
def get_experiments():
    """Section 18.1: Experiment Board view."""
    return projections.get_experiments()


@app.get("/api/v1/decisions/{decision_id}/trace", response_model=Dict[str, Any])
def get_decision_trace(decision_id: str):
    """Section 18.1 & FR-PX-1601: Decision Explorer view with full reasoning chain."""
    trace = projections.get_decision_trace(decision_id)
    if not trace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Decision trace not found: {decision_id}")
    return trace


@app.get("/api/v1/knowledge", response_model=List[Dict[str, Any]])
def get_knowledge():
    """Section 18.1: Knowledge Browser view."""
    return projections.get_knowledge_records()


@app.get("/api/v1/beliefs", response_model=List[Dict[str, Any]])
def get_beliefs():
    """Section 18.1: Belief Inspector view."""
    return projections.get_beliefs()


@app.get("/api/v1/pipelines", response_model=List[Dict[str, Any]])
def get_pipelines():
    """Section 18.1: Pipeline Monitor view."""
    return projections.get_pipelines()


@app.get("/api/v1/costs", response_model=Dict[str, Any])
def get_costs():
    """Section 18.1: Cost Center view."""
    return projections.get_costs()


@app.get("/api/v1/health", response_model=Dict[str, str])
def get_health():
    """Section 18.1: System Health view (`NFR-OBS-003`)."""
    return projections.get_health()


@app.get("/api/v1/approvals", response_model=List[Dict[str, Any]])
def get_approval_inbox():
    """Section 18.1: Approval Inbox view (`FR-PX-1501`)."""
    return projections.get_approval_inbox()


@app.post("/api/v1/approvals/{target_id}/approve", response_model=Dict[str, Any])
def approve_proposal(target_id: str, req: ApprovalActionRequest):
    """FR-PX-1503: Human owner approves gated proposal."""
    audit_logger.log_event(
        event_type=AuditEventType.APPROVAL_GRANTED,
        actor=req.actor,
        target_id=target_id,
        reason=req.reason
    )
    if target_id in projections.approval_inbox:
        del projections.approval_inbox[target_id]
    return {"status": "APPROVED", "target_id": target_id, "actor": req.actor}


@app.post("/api/v1/approvals/{target_id}/reject", response_model=Dict[str, Any])
def reject_proposal(target_id: str, req: ApprovalActionRequest):
    """FR-PX-1503: Human owner rejects gated proposal (produces Level-4 feedback)."""
    audit_logger.log_event(
        event_type=AuditEventType.APPROVAL_REJECTED,
        actor=req.actor,
        target_id=target_id,
        reason=req.reason
    )
    if target_id in projections.approval_inbox:
        del projections.approval_inbox[target_id]
    return {"status": "REJECTED", "target_id": target_id, "actor": req.actor}


@app.post("/api/v1/governance/kill-switch", response_model=Dict[str, Any])
def manage_kill_switch(req: KillSwitchRequest):
    """NFR-SEC-001: Trigger or reset emergency kill switch."""
    if req.action.upper() == "TRIGGER":
        kill_switch.trigger(reason=req.reason)
        projections.health["KillSwitch"] = "ACTIVE_CRITICAL"
        audit_logger.log_event(
            event_type=AuditEventType.KILL_SWITCH_TRIGGERED,
            actor="DASHBOARD_API",
            target_id="system",
            reason=req.reason
        )
        return {"status": "TRIGGERED", "reason": req.reason}
    elif req.action.upper() == "RESET":
        success = kill_switch.reset(authorization_code=req.authorization_code or "")
        if not success:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization code for kill switch reset.")
        projections.health["KillSwitch"] = "INACTIVE"
        audit_logger.log_event(
            event_type=AuditEventType.KILL_SWITCH_RESET,
            actor="DASHBOARD_API",
            target_id="system",
            reason="Kill switch reset"
        )
        return {"status": "RESET", "message": "Normal operations resumed."}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid action. Use 'TRIGGER' or 'RESET'.")
