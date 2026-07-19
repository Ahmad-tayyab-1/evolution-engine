"""
Policy Engine (`FR-PX-1501`, `DP-014`).

Evaluates hypotheses, directives, and narrative content against the `ForbiddenRegistry`,
`ContentPolicy`, and `KillSwitch`. Returns structured evaluation results and logs violations to `AuditLogger`.
"""
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from evolutionos.governance.forbidden_registry import ForbiddenRegistry
from evolutionos.governance.content_policy import ContentPolicy, ApprovalMode
from evolutionos.governance.kill_switch import KillSwitch, KillSwitchActivatedError
from evolutionos.governance.audit_log import AuditLogger, AuditEventType

logger = logging.getLogger("evolutionos.governance.policy_engine")


class PolicyEvaluationResult(BaseModel):
    allowed: bool
    violations: List[str]
    required_approval_mode: ApprovalMode
    target_id: str


class PolicyEngine:
    """Orchestrates policy checks across hypotheses and directives (`DP-014`)."""

    def __init__(
        self,
        registry: Optional[ForbiddenRegistry] = None,
        policy: Optional[ContentPolicy] = None,
        kill_switch: Optional[KillSwitch] = None,
        audit_logger: Optional[AuditLogger] = None
    ):
        self.registry = registry or ForbiddenRegistry()
        self.policy = policy or ContentPolicy()
        self.kill_switch = kill_switch or KillSwitch.get_instance()
        self.audit_logger = audit_logger or AuditLogger()

    def evaluate_proposal(self, target_id: str, content_text: str, parameters: Optional[Dict[str, Any]] = None) -> PolicyEvaluationResult:
        """Evaluate proposal (hypothesis statement, directive topic, or script) against governance constraints."""
        # 1. Enforce Kill Switch (`NFR-SEC-001`)
        if self.kill_switch.is_active():
            self.audit_logger.log_event(
                event_type=AuditEventType.KILL_SWITCH_TRIGGERED,
                actor="POLICY_ENGINE",
                target_id=target_id,
                reason="Proposal blocked because emergency Kill Switch is active."
            )
            raise KillSwitchActivatedError(f"Proposal [{target_id}] blocked: Kill Switch is active.")

        violations = []

        # 2. Check forbidden topics and tactics (`CON-ETH-001`)
        violations.extend(self.registry.check_topic(content_text))
        violations.extend(self.registry.check_tactic(content_text))

        # 3. Check parameter bounds if provided
        if parameters:
            budget = parameters.get("budget_usd", 0.0)
            if budget > self.registry.max_daily_budget_usd:
                violations.append(f"Budget ${budget} exceeds maximum allowed (${self.registry.max_daily_budget_usd})")

            duration = parameters.get("duration_seconds", 0)
            if duration > self.registry.max_video_duration_seconds:
                violations.append(f"Duration {duration}s exceeds maximum allowed ({self.registry.max_video_duration_seconds}s)")

        # Determine approval mode (`FR-PX-1501`, `FR-PX-1502`)
        if violations:
            self.audit_logger.log_event(
                event_type=AuditEventType.POLICY_VIOLATION_BLOCKED,
                actor="POLICY_ENGINE",
                target_id=target_id,
                reason=f"Violations detected: {'; '.join(violations)}",
                metadata={"violations": violations}
            )
            return PolicyEvaluationResult(
                allowed=False,
                violations=violations,
                required_approval_mode=ApprovalMode.GATED_STRICT,
                target_id=target_id
            )

        return PolicyEvaluationResult(
            allowed=True,
            violations=[],
            required_approval_mode=self.policy.minimum_approval_mode,
            target_id=target_id
        )
