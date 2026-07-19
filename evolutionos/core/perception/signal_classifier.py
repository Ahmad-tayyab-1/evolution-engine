"""
Signal Classifier (FR-EC-310).

Classifies integrated observations into Level 1-5 feedback signals and assigns routing targets:
Level 1: Operational -> Platform Health / Monitoring
Level 2: Performance -> Fitness Engine + Reflection Engine
Level 3: Behavioral -> Learning Engine (pattern extraction)
Level 4: Strategic -> Strategy Engine + Belief Engine
Level 5: Evolutionary -> Meta-Reflection + Self-Optimization
"""
from typing import List
from evolutionos.core.domain.ontology import Observation, FeedbackSignal
from evolutionos.core.events.catalog import EventEnvelope
from evolutionos.infrastructure.messaging.broker import MessageBroker


class SignalClassifier:
    """Classifies observations into Level 1-5 feedback levels and routes them."""

    def __init__(self, broker: MessageBroker = None):
        self.broker = broker

    def classify_and_route(self, observations: List[Observation], correlation_id: str) -> List[FeedbackSignal]:
        signals = []
        for obs in observations:
            level, targets = self._determine_level_and_targets(obs)
            summary = f"Level {level} feedback on {obs.metric} ({obs.value} {obs.unit}) for experiment {obs.experiment_id}"
            signal = FeedbackSignal(
                observation_refs=[obs.id],
                feedback_level=level,
                routing_targets=targets,
                summary=summary
            )
            signals.append(signal)

            # Route to broker if configured
            if self.broker:
                for target in targets:
                    env = EventEnvelope(
                        event_type="FeedbackSignalRouted",
                        correlation_id=correlation_id,
                        producer="SignalClassifier",
                        payload={
                            "signal_id": signal.id,
                            "level": level,
                            "target_engine": target,
                            "observation_id": obs.id,
                            "metric": obs.metric,
                            "value": obs.value
                        }
                    )
                    self.broker.publish(f"engine.{target.lower()}", env)
        return signals

    def _determine_level_and_targets(self, obs: Observation) -> tuple[int, List[str]]:
        metric = obs.metric.lower()
        # Level 1: Operational / Health
        if any(m in metric for m in ["error", "latency", "uptime", "status", "quarantine", "quota"]):
            return 1, ["PlatformMonitoring"]
        # Level 5: Evolutionary / Meta
        if any(m in metric for m in ["learning_yield", "calibration_error", "discovery_rate"]):
            return 5, ["MetaReflectionEngine", "SelfOptimization"]
        # Level 4: Strategic / Audience Growth
        if any(m in metric for m in ["subscribers", "audience_growth", "return_rate", "strategic"]):
            return 4, ["StrategyEngine", "BeliefEngine"]
        # Level 3: Behavioral / Pattern Engagement
        if any(m in metric for m in ["retention", "dropoff", "comment", "attention_rate", "engagement"]):
            return 3, ["LearningEngine"]
        # Level 2: Performance (Default primary metrics like CTR / Selection Rate)
        return 2, ["FitnessEngine", "ReflectionEngine"]
