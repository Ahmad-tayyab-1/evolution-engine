"""
Emergency Kill Switch (`NFR-SEC-001`, `DP-014`).

Provides an immediate, high-priority emergency stop across all engines and pipelines.
When activated, `is_active()` returns `True` and raises `KillSwitchActivatedError` on any execution attempt.
"""
import os
import logging
from typing import Optional

logger = logging.getLogger("evolutionos.governance.kill_switch")


class KillSwitchActivatedError(Exception):
    """Raised when an operation is attempted while the Kill Switch is active."""
    pass


class KillSwitch:
    """Singleton-style emergency circuit breaker (`NFR-SEC-001`)."""

    _instance: Optional["KillSwitch"] = None

    def __init__(self, flag_file_path: Optional[str] = None):
        self.flag_file_path = flag_file_path or os.path.join(os.path.expanduser("~"), ".evolutionos_kill_switch")
        self._active_in_memory = False
        self.reason: Optional[str] = None

    @classmethod
    def get_instance(cls) -> "KillSwitch":
        if cls._instance is None:
            cls._instance = KillSwitch()
        return cls._instance

    def trigger(self, reason: str = "EMERGENCY_MANUAL_STOP") -> None:
        """Activate the kill switch immediately (`DP-014`)."""
        self._active_in_memory = True
        self.reason = reason
        logger.critical(f"EMERGENCY KILL SWITCH ACTIVATED (`NFR-SEC-001`): {reason}")
        try:
            with open(self.flag_file_path, "w", encoding="utf-8") as f:
                f.write(f"ACTIVE: {reason}\n")
        except Exception as e:
            logger.error(f"Failed to write kill switch flag file: {e}")

    def reset(self, authorization_code: str = "CONFIRM_RESET") -> bool:
        """Deactivate the kill switch with confirmation."""
        if authorization_code != "CONFIRM_RESET":
            logger.warning("Invalid authorization code for kill switch reset.")
            return False
        self._active_in_memory = False
        self.reason = None
        if os.path.exists(self.flag_file_path):
            try:
                os.remove(self.flag_file_path)
            except Exception as e:
                logger.error(f"Failed to remove kill switch flag file: {e}")
        logger.info("Emergency Kill Switch reset. Normal operations may resume.")
        return True

    def is_active(self) -> bool:
        """Check if kill switch is active in memory or on filesystem."""
        if self._active_in_memory:
            return True
        return os.path.exists(self.flag_file_path)

    def enforce(self) -> None:
        """Raise KillSwitchActivatedError if active (`NFR-SEC-001`)."""
        if self.is_active():
            raise KillSwitchActivatedError(f"Operation blocked: Kill Switch is ACTIVE ({self.reason or 'File flag present'})")
