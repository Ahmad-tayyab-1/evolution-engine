"""
Configuration and Settings Loader (INF-CFG-004, INF-SEC-001).

Loads canonical defaults from `defaults.yaml`, overrides with environment variables / SOPS,
validates schema rules, and provides secret redaction utilities for loggers (`INF-LOG-003`).
"""
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional
import yaml


class ConfigError(Exception):
    """Raised when configuration validation fails."""
    pass


def load_defaults() -> Dict[str, Any]:
    """Load canonical defaults from config/defaults.yaml."""
    config_path = Path(__file__).parent / "defaults.yaml"
    if not config_path.exists():
        raise ConfigError(f"defaults.yaml not found at {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


class Settings:
    """System-wide validated configuration instance."""

    def __init__(self, overrides: Optional[Dict[str, Any]] = None):
        self.raw_config = load_defaults()
        if overrides:
            self._deep_update(self.raw_config, overrides)
        self._validate_and_bind()

    def _deep_update(self, base: Dict[str, Any], update: Dict[str, Any]) -> None:
        for k, v in update.items():
            if isinstance(v, dict) and k in base and isinstance(base[k], dict):
                self._deep_update(base[k], v)
            else:
                base[k] = v

    def _validate_and_bind(self) -> None:
        # Bind Evolution params
        evo = self.raw_config.get("evolution", {})
        self.min_exploration_rate = float(os.getenv("EVO_MIN_EXPLORATION", evo.get("min_exploration_rate", 0.10)))
        self.max_exploration_rate = float(os.getenv("EVO_MAX_EXPLORATION", evo.get("max_exploration_rate", 0.40)))
        self.default_exploration_rate = float(os.getenv("EVO_DEFAULT_EXPLORATION", evo.get("default_exploration_rate", 0.15)))
        self.meta_reflection_interval = int(evo.get("meta_reflection_interval", 20))
        self.default_mutation_budget = int(evo.get("default_mutation_budget", 1))

        if not (0.0 <= self.min_exploration_rate <= self.max_exploration_rate <= 1.0):
            raise ConfigError(
                f"Invalid exploration rate bounds: min={self.min_exploration_rate}, max={self.max_exploration_rate}"
            )

        # Bind Knowledge params
        knw = self.raw_config.get("knowledge", {})
        self.min_evidence_count = int(knw.get("min_evidence_count", 3))
        self.consolidation_similarity_threshold = float(knw.get("consolidation_similarity_threshold", 0.85))
        self.decay_window_days = int(knw.get("decay_window_days", 90))
        self.belief_decay_days = self.decay_window_days
        self.deprecation_threshold = float(knw.get("deprecation_threshold", 0.35))
        self.confidence_floor = float(knw.get("confidence_floor", 0.01))
        self.confidence_ceiling = float(knw.get("confidence_ceiling", 0.99))

        # Bind Belief params
        bel = self.raw_config.get("belief", {})
        self.learning_rate = float(bel.get("learning_rate", 0.15))
        self.prior_pull = float(bel.get("prior_pull", 0.05))

        # Bind Fitness weights
        fit = self.raw_config.get("fitness", {})
        self.fitness_weights = fit.get("weights", {
            "learning_yield": 0.35,
            "prediction_accuracy": 0.25,
            "performance_delta": 0.20,
            "strategic_alignment": 0.15,
            "cost_efficiency": 0.05
        })
        self.goodhart_alert_threshold = float(fit.get("goodhart_alert_threshold", 0.25))

        # Bind Governance params
        gov = self.raw_config.get("governance", {})
        self.default_approval_mode = os.getenv("DEFAULT_APPROVAL_MODE", gov.get("default_approval_mode", "GATED"))
        self.max_publications_per_day = int(gov.get("max_publications_per_day", 3))
        self.max_cost_per_experiment_usd = float(gov.get("max_cost_per_experiment_usd", 2.00))

        # Bind Providers
        prov = self.raw_config.get("providers", {})
        self.provider_routing = prov.get("routing", {})
        self.cache_ttl_seconds = int(prov.get("cache_ttl_seconds", 604800))

        # Bind Simulation params
        sim = self.raw_config.get("simulation", {})
        self.sim_min_discovery_rate = float(sim.get("min_discovery_rate", 0.80))
        self.sim_max_cycles = int(sim.get("max_simulation_cycles", 50))
        self.sim_max_calibration_error = float(sim.get("max_calibration_error", 0.15))
        self.sim_noise_stddev = float(sim.get("default_noise_stddev", 0.03))

        # Database & Messaging connections (INF-DB-001, ADR-014, ADR-015)
        self.db_url = os.getenv("DB_URL", "sqlite:///./evolutionos_dev.db")
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.use_memory_broker = os.getenv("USE_MEMORY_BROKER", "true").lower() == "true"

    def get_secret(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Load secret from env or SOPS secure storage (INF-SEC-001)."""
        val = os.getenv(key, default)
        return val


# Global singleton setting instance
settings = Settings()


def redact_secrets(text: str) -> str:
    """INF-LOG-003: Redact sensitive API keys, tokens, and passwords from log strings."""
    if not text or not isinstance(text, str):
        return str(text)

    # Patterns for API keys and tokens
    patterns = [
        (r"(?i)(api[_-]?key|secret|token|password)[\s:=]+([a-zA-Z0-9_\-\.]{12,})", r"\1=[REDACTED]"),
        (r"(AIza[0-9A-Za-z-_]{35})", r"[REDACTED_GOOGLE_KEY]"),
        (r"(gsk_[a-zA-Z0-9]{48,})", r"[REDACTED_GROQ_KEY]"),
        (r"(sk-[a-zA-Z0-9]{32,})", r"[REDACTED_OPENAI_KEY]"),
    ]
    redacted = text
    for pattern, replacement in patterns:
        redacted = re.sub(pattern, replacement, redacted)
    return redacted
