"""
CQRS Projections (`Section 18.2`, `FR-PX-1601`, `NFR-OBS-003`).

Builds and maintains read-only materialized views by subscribing to event streams
(`core.events`, `execution.events`, `governance.events`).
The dashboard queries these projections exclusively and never interacts with the Core write model.
"""
import time
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from evolutionos.infrastructure.messaging.broker import MessageBroker
from evolutionos.core.events.catalog import EventEnvelope

logger = logging.getLogger("evolutionos.dashboard.projections")


class CQRSProjectionEngine:
    """Read-only projections engine fed by event subscription (`Section 18.2`)."""

    def __init__(self, broker: Optional[MessageBroker] = None):
        self.broker = broker
        # Projections
        self.overview: Dict[str, Any] = {
            "fitness_trend": [],
            "total_knowledge_records": 0,
            "mean_prediction_accuracy": 1.0,
            "active_cycle": 0,
            "last_updated": time.time()
        }
        self.experiments: Dict[str, Dict[str, Any]] = {}       # id -> experiment projection
        self.decisions: Dict[str, Dict[str, Any]] = {}         # id -> decision trace projection (`FR-PX-1601`)
        self.knowledge: Dict[str, Dict[str, Any]] = {}         # id -> knowledge record projection
        self.beliefs: Dict[str, Dict[str, Any]] = {}           # id -> belief projection
        self.pipelines: Dict[str, Dict[str, Any]] = {}         # id -> workflow status projection
        self.costs: Dict[str, Any] = {
            "total_spend_usd": 0.0,
            "by_provider": {},
            "by_experiment": {}
        }
        self.health: Dict[str, str] = {
            "KnowledgeEngine": "HEALTHY",
            "BeliefEngine": "HEALTHY",
            "HypothesisEngine": "HEALTHY",
            "StrategyEngine": "HEALTHY",
            "DecisionEngine": "HEALTHY",
            "ExperimentEngine": "HEALTHY",
            "WorkflowOrchestrator": "HEALTHY",
            "KillSwitch": "INACTIVE"
        }
        self.approval_inbox: Dict[str, Dict[str, Any]] = {}    # id -> pending proposal

        if self.broker:
            self._subscribe_to_streams()

    def _subscribe_to_streams(self) -> None:
        self.broker.subscribe("core.events", "dashboard", "cqrs_projections", self._handle_core_event)
        self.broker.subscribe("execution.events", "dashboard", "cqrs_projections", self._handle_execution_event)
        self.broker.subscribe("governance.events", "dashboard", "cqrs_projections", self._handle_governance_event)

    def _handle_core_event(self, envelope: EventEnvelope) -> None:
        payload = envelope.payload
        etype = envelope.event_type

        if etype == "FitnessComputed":
            scalar = payload.get("scalar_score", 0.0)
            self.overview["fitness_trend"].append({
                "occurred_at": envelope.occurred_at,
                "experiment_id": payload.get("experiment_id"),
                "scalar_score": scalar
            })
            self.overview["last_updated"] = time.time()

        elif etype == "DecisionMade":
            dec_id = payload.get("decision_id", f"dec_{envelope.correlation_id}")
            # Store complete reasoning chain (`FR-PX-1601`)
            self.decisions[dec_id] = {
                "decision_id": dec_id,
                "selected_candidate_id": payload.get("selected_candidate_id"),
                "all_candidates": payload.get("candidates", []),
                "evidence_ids": payload.get("evidence_ids", []),
                "confidence": payload.get("confidence", 0.8),
                "reasoning_summary": payload.get("reasoning_summary", ""),
                "occurred_at": envelope.occurred_at
            }

        elif etype in ["KnowledgeRecordCreated", "KnowledgeRecordConsolidated"]:
            rec_id = payload.get("record_id", f"kr_{envelope.correlation_id}")
            self.knowledge[rec_id] = payload
            self.overview["total_knowledge_records"] = len(self.knowledge)

        elif etype == "BeliefUpdated":
            b_id = payload.get("belief_id", f"b_{envelope.correlation_id}")
            self.beliefs[b_id] = payload

        elif etype == "ExperimentStateChanged":
            exp_id = payload.get("experiment_id")
            if exp_id:
                if exp_id not in self.experiments:
                    self.experiments[exp_id] = {"id": exp_id, "state": payload.get("new_state")}
                else:
                    self.experiments[exp_id]["state"] = payload.get("new_state")

    def _handle_execution_event(self, envelope: EventEnvelope) -> None:
        payload = envelope.payload
        if envelope.event_type == "PipelineStageCompleted":
            p_id = payload.get("directive_id", "default_pipeline")
            self.pipelines[p_id] = payload

        elif envelope.event_type == "LLMCostLogged":
            cost = payload.get("cost_usd", 0.0)
            provider = payload.get("provider", "unknown")
            exp_id = payload.get("experiment_id", "exp_default")
            self.costs["total_spend_usd"] += cost
            self.costs["by_provider"][provider] = self.costs["by_provider"].get(provider, 0.0) + cost
            self.costs["by_experiment"][exp_id] = self.costs["by_experiment"].get(exp_id, 0.0) + cost

    def _handle_governance_event(self, envelope: EventEnvelope) -> None:
        payload = envelope.payload
        if envelope.event_type == "ProposalGated":
            target_id = payload.get("target_id", f"target_{envelope.correlation_id}")
            self.approval_inbox[target_id] = payload

        elif envelope.event_type in ["ApprovalGranted", "ApprovalRejected"]:
            target_id = payload.get("target_id")
            if target_id and target_id in self.approval_inbox:
                del self.approval_inbox[target_id]

        elif envelope.event_type == "KillSwitchTriggered":
            self.health["KillSwitch"] = "ACTIVE_CRITICAL"

    def get_overview(self) -> Dict[str, Any]:
        return self.overview

    def get_experiments(self) -> List[Dict[str, Any]]:
        return list(self.experiments.values())

    def get_decision_trace(self, decision_id: str) -> Optional[Dict[str, Any]]:
        """FR-PX-1601: Complete reasoning chain within 3 clicks."""
        return self.decisions.get(decision_id)

    def get_knowledge_records(self) -> List[Dict[str, Any]]:
        return list(self.knowledge.values())

    def get_beliefs(self) -> List[Dict[str, Any]]:
        return list(self.beliefs.values())

    def get_pipelines(self) -> List[Dict[str, Any]]:
        return list(self.pipelines.values())

    def get_costs(self) -> Dict[str, Any]:
        return self.costs

    def get_health(self) -> Dict[str, str]:
        return self.health

    def get_approval_inbox(self) -> List[Dict[str, Any]]:
        return list(self.approval_inbox.values())
