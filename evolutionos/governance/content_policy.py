"""
Content Policy & Safety Tiers (`FR-PX-603`, `FR-PX-1501`).

Defines safety requirements, license standards, and approval modes (`AUTONOMOUS`, `NOTIFY`, `GATED`, `GATED_STRICT`).
"""
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class ApprovalMode(str, Enum):
    """FR-PX-1501: Human approval framework modes."""
    AUTONOMOUS = "AUTONOMOUS"     # No human gate (`target state, NFR-AUT-001`)
    NOTIFY = "NOTIFY"             # Publish + notify owner
    GATED = "GATED"               # Hold at AWAITING_APPROVAL until approve/reject/timeout
    GATED_STRICT = "GATED_STRICT" # Hold indefinitely until explicit human signature


class LicenseRequirement(str, Enum):
    """FR-PX-603: Commercial license compatibility classes."""
    COMMERCIAL_COMPATIBLE = "COMMERCIAL_COMPATIBLE"
    OPEN_SOURCE_BY_SA = "OPEN_SOURCE_BY_SA"
    STRICT_PROPRIETARY = "STRICT_PROPRIETARY"


class ContentPolicy(BaseModel):
    """Policy rules governing visual and narrative generation."""
    policy_id: str = "default_content_policy"
    minimum_approval_mode: ApprovalMode = ApprovalMode.GATED
    require_commercial_compatible_license: bool = True
    enforce_fact_check_single_source_minimum: bool = True
    max_claim_confidence_without_peer_review: float = 0.90
    allow_synthetic_voice: bool = True
