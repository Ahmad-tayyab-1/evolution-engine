"""
Decision Engine (FR-EC-210, FR-EC-211, FR-EC-212).

Enforces mandatory 8-step decision protocol:
1. FRAME -> 2. RETRIEVE -> 3. GENERATE (>=3 candidates) -> 4. SCORE -> 5. RISK -> 6. SELECT -> 7. RECORD -> 8. PREDICT.
Enforces minimum exploration rate (default 15%) and adaptive adjustments based on fitness plateaus.
"""
import random
from typing import Any, Dict, List, Optional
from evolutionos.core.domain.ontology import Decision, Candidate, Prediction, MetricPrediction
from evolutionos.core.events.catalog import DecisionMade, EventEnvelope
from evolutionos.core.learning.knowledge_engine import KnowledgeEngine
from evolutionos.core.reasoning.belief_engine import BeliefEngine
from evolutionos.infrastructure.messaging.broker import MessageBroker
from evolutionos.config.settings import settings


class DecisionEngine:
    """Orchestrates the 8-step Decision Protocol with exploration vs exploitation policies."""

    def __init__(
        self,
        knowledge_engine: KnowledgeEngine,
        belief_engine: BeliefEngine,
        broker: Optional[MessageBroker] = None
    ):
        self.knowledge_engine = knowledge_engine
        self.belief_engine = belief_engine
        self.broker = broker
        self.decisions: Dict[str, Decision] = {}
        self.exploration_rate = settings.default_exploration_rate

    def adjust_exploration_rate(self, is_plateaued: bool, is_volatile: bool) -> float:
        """FR-EC-212: Adaptive exploration rate when plateau or volatility is detected."""
        if is_plateaued:
            self.exploration_rate = min(0.50, self.exploration_rate + 0.10)
        elif is_volatile:
            self.exploration_rate = max(0.05, self.exploration_rate - 0.05)
        return self.exploration_rate

    def make_decision(
        self,
        decision_type: str,
        context: Dict[str, Any],
        candidates: List[Candidate],
        prediction_spec: Optional[Dict[str, Any]] = None,
        correlation_id: str = "none"
    ) -> Decision:
        """FR-EC-210: Execute 8-Step Decision Protocol."""
        # Step 1: FRAME
        frame_ctx = context.copy()

        # Step 2: RETRIEVE relevant knowledge and beliefs
        # Gather active record IDs
        knowledge_used = [kr.id for kr in self.knowledge_engine.records.values() if kr.status.value == "ACTIVE"][:5]
        beliefs_used = [b.id for b in self.belief_engine.beliefs.values() if b.status.value == "ACTIVE"][:5]

        # Step 3: GENERATE (Ensure >= 3 candidates per FR-EC-210 / FR-013)
        if len(candidates) < 3:
            raise ValueError(f"FR-EC-210 Violation: At least 3 candidates required, got {len(candidates)}.")

        # Step 4: SCORE candidates
        scored_candidates = []
        for cand in candidates:
            # Score computed from value/novelty minus risk penalty
            total_score = cand.score - (cand.risk * 0.5) + (cand.novelty * 0.2)
            cand.score_breakdown["computed_total"] = total_score
            scored_candidates.append(cand)

        # Sort descending by computed score
        scored_candidates.sort(key=lambda c: c.score_breakdown.get("computed_total", c.score), reverse=True)

        # Step 5: RISK assessment across top candidates
        avg_risk = sum(c.risk for c in scored_candidates) / len(scored_candidates)

        # Step 6: SELECT per active policy (Exploit vs Explore)
        # With probability exploration_rate, select a non-top candidate (e.g., 2nd or 3rd best)
        do_explore = random.random() < self.exploration_rate
        if do_explore and len(scored_candidates) > 1:
            policy = "EXPLORE"
            selected_candidate = random.choice(scored_candidates[1:])
        else:
            policy = "EXPLOIT"
            selected_candidate = scored_candidates[0]

        rejection_reasons = {}
        for c in scored_candidates:
            if c.id != selected_candidate.id:
                rejection_reasons[c.id] = {
                    "reason": "Lower rank in EXPLOIT mode" if policy == "EXPLOIT" else "Not chosen during exploration",
                    "score_diff": selected_candidate.score_breakdown.get("computed_total", 0) - c.score_breakdown.get("computed_total", 0)
                }

        # Step 8: PREDICT measurable outcome
        prediction = None
        if prediction_spec:
            metric_preds = [
                MetricPrediction(metric=k, expected_value=v, expected_range={"min": v * 0.9, "max": v * 1.1})
                for k, v in prediction_spec.items() if isinstance(v, (int, float))
            ]
            prediction = Prediction(
                experiment_id=context.get("experiment_id", "none"),
                hypothesis_id=context.get("hypothesis_id", "none"),
                metric_predictions=metric_preds,
                knowledge_used=knowledge_used,
                beliefs_used=beliefs_used
            )

        # Step 7: RECORD DecisionRecord (FR-EC-211)
        decision = Decision(
            type=decision_type,
            context=frame_ctx,
            candidates=candidates,
            scores=[c.score_breakdown for c in scored_candidates],
            knowledge_used=knowledge_used,
            beliefs_used=beliefs_used,
            policy=policy,
            selected_candidate_id=selected_candidate.id,
            rejection_reasons=rejection_reasons,
            risk_score=avg_risk,
            prediction=prediction
        )
        self.decisions[decision.id] = decision

        # Emit DecisionMade event
        event = DecisionMade(
            decision_id=decision.id,
            decision_type=decision_type,
            selected_option=str(selected_candidate.value),
            policy_used=policy
        )
        if self.broker:
            env = event.wrap(producer="DecisionEngine", correlation_id=correlation_id)
            self.broker.publish("core.events", env)

        return decision
