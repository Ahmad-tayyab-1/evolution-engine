"""
Governance, Safety, and Dashboard API E2E Verification (`Milestone v1.0`).

Verifies:
1. Forbidden Registry (`CON-ETH-001`) and Content Policy blocking unethical tactics and parameter bounds.
2. Emergency Kill Switch (`NFR-SEC-001`) interrupting operations and raising `KillSwitchActivatedError`.
3. Append-only Audit Trail (`DP-014`, `FR-PX-1503`) recording all policy checks, rejections, and triggers.
4. Read-only CQRS Projections (`Section 18.2`) fed via `MessageBroker` event subscription.
5. FastAPI Dashboard REST endpoints (`Section 18.1`, `FR-PX-1601`) exposing projections and governance actions.
"""
import pytest
from fastapi.testclient import TestClient
from evolutionos.governance.forbidden_registry import ForbiddenRegistry
from evolutionos.governance.content_policy import ContentPolicy, ApprovalMode
from evolutionos.governance.kill_switch import KillSwitch, KillSwitchActivatedError
from evolutionos.governance.audit_log import AuditLogger, AuditEventType
from evolutionos.governance.policy_engine import PolicyEngine, PolicyEvaluationResult
from evolutionos.dashboard.api.projections import CQRSProjectionEngine
from evolutionos.dashboard.api.main import app, kill_switch, projections, audit_logger, broker
from evolutionos.core.events.catalog import EventEnvelope


def test_forbidden_registry_and_policy_engine_evaluations():
    """Verify CON-ETH-001 forbidden topic/tactic detection and budget bound limits (`DP-014`)."""
    registry = ForbiddenRegistry()
    policy = ContentPolicy()
    audit = AuditLogger()
    engine = PolicyEngine(registry=registry, policy=policy, audit_logger=audit)

    # 1. Clean proposal within bounds
    res_clean = engine.evaluate_proposal(target_id="prop_clean", content_text="Standard educational tutorial about Python")
    assert res_clean.allowed is True
    assert len(res_clean.violations) == 0
    assert res_clean.required_approval_mode == ApprovalMode.GATED

    # 2. Forbidden topic check
    res_hate = engine.evaluate_proposal(target_id="prop_hate", content_text="Video featuring hate_speech or doxxing")
    assert res_hate.allowed is False
    assert any("hate_speech" in v for v in res_hate.violations)
    assert res_hate.required_approval_mode == ApprovalMode.GATED_STRICT

    # 3. Forbidden tactic check
    res_clickbait = engine.evaluate_proposal(target_id="prop_tactic", content_text="Use deceptive_clickbait and fake_emergency")
    assert res_clickbait.allowed is False
    assert any("deceptive_clickbait" in v for v in res_clickbait.violations)

    # 4. Parameter bound violation ($500 budget > $100 limit)
    res_budget = engine.evaluate_proposal(
        target_id="prop_budget",
        content_text="High budget campaign",
        parameters={"budget_usd": 500.0, "duration_seconds": 600}
    )
    assert res_budget.allowed is False
    assert any("exceeds maximum allowed" in v for v in res_budget.violations)

    # Verify audit log recorded blocked violations
    events = audit.get_events_for_target("prop_budget")
    assert len(events) == 1
    assert events[0].event_type == AuditEventType.POLICY_VIOLATION_BLOCKED


def test_emergency_kill_switch_enforcement(tmp_path):
    """Verify NFR-SEC-001 emergency circuit breaker halts policy checks and execution attempts immediately."""
    flag_path = str(tmp_path / "test_kill_switch")
    ks = KillSwitch(flag_file_path=flag_path)
    engine = PolicyEngine(kill_switch=ks)

    assert ks.is_active() is False

    # Trigger emergency kill switch
    ks.trigger(reason="Anomalous loop detected")
    assert ks.is_active() is True

    # Any proposal evaluation attempts must raise KillSwitchActivatedError immediately
    with pytest.raises(KillSwitchActivatedError):
        engine.evaluate_proposal("prop_any", "Safe content")

    # Verify enforce() raises explicitly
    with pytest.raises(KillSwitchActivatedError):
        ks.enforce()

    # Reset kill switch with correct authorization code
    assert ks.reset(authorization_code="WRONG_CODE") is False
    assert ks.is_active() is True

    assert ks.reset(authorization_code="CONFIRM_RESET") is True
    assert ks.is_active() is False


def test_cqrs_projections_and_dashboard_rest_api():
    """Verify CQRS read-only projections and FastAPI endpoints (`Section 18.1`, `Section 18.2`, `FR-PX-1601`)."""
    client = TestClient(app)

    # Publish events into the broker to feed CQRS projection views
    broker.publish("core.events", EventEnvelope(
        event_type="DecisionMade",
        correlation_id="corr_101",
        producer="DecisionEngine",
        payload={
            "decision_id": "dec_trace_101",
            "selected_candidate_id": "cand_winner",
            "candidates": ["cand_winner", "cand_loser"],
            "evidence_ids": ["kr_10", "kr_11"],
            "confidence": 0.88,
            "reasoning_summary": "Selected candidate due to high historical CTR evidence and strong belief calibration."
        }
    ))

    broker.publish("core.events", EventEnvelope(
        event_type="FitnessComputed",
        correlation_id="corr_102",
        producer="FitnessEngine",
        payload={"experiment_id": "exp_fitness_1", "scalar_score": 0.92}
    ))

    broker.publish("execution.events", EventEnvelope(
        event_type="LLMCostLogged",
        correlation_id="corr_103",
        producer="MultiProviderLLMRouter",
        payload={"provider": "anthropic", "cost_usd": 0.045, "experiment_id": "exp_fitness_1"}
    ))

    # Query overview endpoint
    resp = client.get("/api/v1/overview")
    assert resp.status_code == 200
    overview_data = resp.json()
    assert len(overview_data["fitness_trend"]) >= 1
    assert overview_data["fitness_trend"][-1]["scalar_score"] == 0.92

    # Query Decision Trace endpoint (`FR-PX-1601`: verify complete reasoning chain within 3 clicks)
    resp_trace = client.get("/api/v1/decisions/dec_trace_101/trace")
    assert resp_trace.status_code == 200
    trace_data = resp_trace.json()
    assert trace_data["selected_candidate_id"] == "cand_winner"
    assert trace_data["confidence"] == 0.88
    assert "reasoning_summary" in trace_data

    # Query Cost Center endpoint
    resp_costs = client.get("/api/v1/costs")
    assert resp_costs.status_code == 200
    cost_data = resp_costs.json()
    assert cost_data["total_spend_usd"] >= 0.045
    assert cost_data["by_provider"]["anthropic"] >= 0.045

    # Query System Health endpoint
    resp_health = client.get("/api/v1/health")
    assert resp_health.status_code == 200
    health_data = resp_health.json()
    assert health_data["KnowledgeEngine"] == "HEALTHY"


def test_dashboard_governance_approval_and_kill_switch_api():
    """Verify dashboard API endpoints for human approval, rejection, and kill switch control (`FR-PX-1503`)."""
    client = TestClient(app)

    # Seed approval inbox with a pending proposal
    projections.approval_inbox["prop_gate_1"] = {
        "target_id": "prop_gate_1",
        "statement": "Test hypothesis A",
        "required_mode": "GATED"
    }

    # Verify pending item in inbox
    resp_inbox = client.get("/api/v1/approvals")
    assert resp_inbox.status_code == 200
    assert len(resp_inbox.json()) >= 1

    # Approve via endpoint
    resp_appr = client.post("/api/v1/approvals/prop_gate_1/approve", json={"actor": "HUMAN_OWNER", "reason": "Looks good"})
    assert resp_appr.status_code == 200
    assert resp_appr.json()["status"] == "APPROVED"
    assert "prop_gate_1" not in projections.approval_inbox

    # Test Kill Switch trigger via API
    resp_ks = client.post("/api/v1/governance/kill-switch", json={"action": "TRIGGER", "reason": "Test trigger via API"})
    assert resp_ks.status_code == 200
    assert kill_switch.is_active() is True
    assert projections.health["KillSwitch"] == "ACTIVE_CRITICAL"

    # Reset Kill Switch via API
    resp_reset = client.post("/api/v1/governance/kill-switch", json={"action": "RESET", "authorization_code": "CONFIRM_RESET"})
    assert resp_reset.status_code == 200
    assert kill_switch.is_active() is False
    assert projections.health["KillSwitch"] == "INACTIVE"
