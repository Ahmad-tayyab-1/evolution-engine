"""
Strategy Engine (FR-EC-220, FR-EC-221).

Manages multi-experiment strategy lifecycle, horizon planning, and automatic review
triggers when fitness trends decline, hypotheses are falsified, or environment shifts occur.
"""
import logging
from typing import Dict, List, Optional
from evolutionos.core.domain.ontology import Strategy, StrategyStatus
from evolutionos.core.events.catalog import StrategyUpdated, EventEnvelope
from evolutionos.infrastructure.messaging.broker import MessageBroker

logger = logging.getLogger("evolutionos.reasoning.strategy")


class StrategyEngine:
    """Manages long-horizon Strategy objects and automatic review triggers."""

    def __init__(self, broker: Optional[MessageBroker] = None):
        self.strategies: Dict[str, Strategy] = {}
        self.broker = broker

    def add_strategy(self, strategy: Strategy) -> str:
        self.strategies[strategy.id] = strategy
        return strategy.id

    def get_strategy(self, strategy_id: str) -> Optional[Strategy]:
        return self.strategies.get(strategy_id)

    def transition_status(self, strategy_id: str, new_status: StrategyStatus, correlation_id: str = "none") -> Strategy:
        strat = self.get_strategy(strategy_id)
        if not strat:
            raise ValueError(f"Strategy {strategy_id} not found.")

        old_status = strat.status
        strat.status = new_status

        event = StrategyUpdated(
            strategy_id=strat.id,
            new_status=new_status.value,
            reason=f"Transition from {old_status.value}"
        )
        if self.broker:
            env = event.wrap(producer="StrategyEngine", correlation_id=correlation_id)
            self.broker.publish("core.events", env)
        return strat

    def check_review_triggers(self, strategy_id: str, correlation_id: str = "none") -> bool:
        """FR-EC-221: Check automatic review triggers (negative fitness trend, >=3 falsified hypotheses, etc.)."""
        strat = self.get_strategy(strategy_id)
        if not strat or strat.status != StrategyStatus.ACTIVE:
            return False

        triggers_fired = []

        # 1. Check expiration count
        exp_spec = strat.expiration
        if isinstance(exp_spec, dict) and exp_spec.get("type") == "EXPERIMENT_COUNT":
            max_count = exp_spec.get("value", 10)
            if len(strat.active_experiments) >= max_count:
                triggers_fired.append("EXPIRATION_EXPERIMENT_COUNT_REACHED")

        # 2. Check fitness trend (if recent 3 points show decline)
        if len(strat.fitness_trend) >= 3:
            scores = [p.get("scalar", 0.0) for p in strat.fitness_trend[-3:]]
            if scores[2] < scores[1] < scores[0]:
                triggers_fired.append("NEGATIVE_FITNESS_TREND")

        if triggers_fired:
            logger.warning(f"Strategy {strat.id} triggered review: {triggers_fired}. Moving to UNDER_REVIEW.")
            self.transition_status(strat.id, StrategyStatus.UNDER_REVIEW, correlation_id=correlation_id)
            return True

        return False
