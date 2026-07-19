"""
Forbidden Registry (`CON-ETH-001`, `DP-014`).

Registry of strictly disallowed topics, unethical engagement manipulation tactics,
and dangerous parameter bounds. Any hypothesis or directive referencing these is blocked.
"""
from typing import Set, List, Dict, Any


class ForbiddenRegistry:
    """Immutable registry of disallowed actions, topics, and parameter manipulations."""

    def __init__(self):
        # Disallowed topics and keywords (`CON-ETH-001`)
        self.disallowed_topics: Set[str] = {
            "hate_speech", "harassment", "doxxing", "illegal_acts",
            "self_harm", "financial_fraud", "unverified_medical_claims"
        }

        # Disallowed psychological/engagement tactics
        self.disallowed_tactics: Set[str] = {
            "deceptive_clickbait", "fake_emergency", "deepfake_impersonation",
            "subliminal_messaging", "manufactured_outrage"
        }

        # Dangerous parameter bounds
        self.max_daily_budget_usd: float = 100.0
        self.max_video_duration_seconds: int = 7200

    def check_topic(self, topic: str) -> List[str]:
        """Check topic string for forbidden terms or concepts."""
        violations = []
        lower_topic = topic.lower()
        for dt in self.disallowed_topics:
            if dt in lower_topic:
                violations.append(f"Forbidden topic detected: {dt}")
        return violations

    def check_tactic(self, tactic_or_statement: str) -> List[str]:
        """Check hypothesis or strategy description for unethical tactics."""
        violations = []
        lower_stmt = tactic_or_statement.lower()
        for dt in self.disallowed_tactics:
            if dt in lower_stmt:
                violations.append(f"Forbidden tactic detected: {dt}")
        return violations
