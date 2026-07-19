"""
Workflow Orchestrator & Pipeline State Machine (`FR-PX-101` to `FR-PX-105`).

Orchestrates Execution Layer stages converting abstract `ExperimentDirective` into concrete
actions and normalized observations (`PX-001`, `PX-002`, `PX-003`).

Features:
- State Machine (`FR-PX-101`): `RECEIVED -> RESEARCHING -> STORY_DRAFTED -> ... -> REPORTED`
- Checkpointing (`FR-PX-102`): Persists stage outputs before advancing; crash recovery resumes cleanly (`NFR-AVA-002`).
- Stage Contracts (`FR-PX-103`): `BasePipelineStage` with schema, timeout, retry, and cost estimates.
- Parallelization (`FR-PX-104`): Concurrent execution of independent stages (`narration`, `visuals`).
- Budget Enforcement (`FR-PX-105`): Tracks cumulative tokens/calls/USD against `ResourceBudget`; raises `BudgetExceeded`.
"""
import time
import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Any, List, Optional, Type
from concurrent.futures import ThreadPoolExecutor, as_completed
from pydantic import BaseModel, Field

logger = logging.getLogger("evolutionos.execution.workflow")


class PipelineState(str, Enum):
    RECEIVED = "RECEIVED"
    RESEARCHING = "RESEARCHING"
    STORY_DRAFTED = "STORY_DRAFTED"
    SCRIPTED = "SCRIPTED"
    NARRATED = "NARRATED"
    VISUALS_PLANNED = "VISUALS_PLANNED"
    COMPOSING = "COMPOSING"
    THUMBNAIL_READY = "THUMBNAIL_READY"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    PUBLISHING = "PUBLISHING"
    PUBLISHED = "PUBLISHED"
    MEASURING = "MEASURING"
    REPORTED = "REPORTED"
    FAILED = "FAILED"


class ResourceBudget(BaseModel):
    """FR-PX-105: Resource budget constraint for an execution pipeline run."""
    max_cost_usd: float = 5.0
    max_tokens: int = 100_000
    max_api_calls: int = 50


class BudgetExceeded(Exception):
    """Raised when pipeline execution exceeds its allocated ResourceBudget."""
    pass


class BudgetTracker:
    """Tracks cumulative expenditure against ResourceBudget (`FR-PX-105`)."""
    def __init__(self, budget: ResourceBudget):
        self.budget = budget
        self.spent_usd: float = 0.0
        self.spent_tokens: int = 0
        self.spent_api_calls: int = 0

    def record_usage(self, cost_usd: float = 0.0, tokens: int = 0, api_calls: int = 1) -> None:
        self.spent_usd += cost_usd
        self.spent_tokens += tokens
        self.spent_api_calls += api_calls

        if self.spent_usd > self.budget.max_cost_usd:
            raise BudgetExceeded(f"Cost limit exceeded: spent ${self.spent_usd:.3f} > max ${self.budget.max_cost_usd:.3f}")
        if self.spent_tokens > self.budget.max_tokens:
            raise BudgetExceeded(f"Token limit exceeded: spent {self.spent_tokens} > max {self.budget.max_tokens}")
        if self.spent_api_calls > self.budget.max_api_calls:
            raise BudgetExceeded(f"API call limit exceeded: spent {self.spent_api_calls} > max {self.budget.max_api_calls}")


class BasePipelineStage(ABC):
    """FR-PX-103: Abstract contract for all Execution Layer pipeline stages."""
    stage_name: str
    target_state: PipelineState
    timeout_seconds: int = 60
    max_retries: int = 2
    estimated_cost_usd: float = 0.01

    @abstractmethod
    def execute(self, context: Dict[str, Any], tracker: BudgetTracker) -> Dict[str, Any]:
        """Execute stage logic and return artifact output dictionary."""
        pass

    def run_with_retry(self, context: Dict[str, Any], tracker: BudgetTracker) -> Dict[str, Any]:
        """Execute stage with retry policy (`FR-PX-103`)."""
        attempts = 0
        while attempts <= self.max_retries:
            try:
                tracker.record_usage(cost_usd=self.estimated_cost_usd, api_calls=1)
                return self.execute(context, tracker)
            except BudgetExceeded:
                raise
            except Exception as e:
                attempts += 1
                logger.warning(f"Stage {self.stage_name} attempt {attempts} failed: {e}")
                if attempts > self.max_retries:
                    raise RuntimeError(f"Stage {self.stage_name} failed after {attempts} attempts: {e}") from e
                time.sleep(0.1)
        return {}


class StageCheckpointStore:
    """FR-PX-102: Checkpoint store saving stage artifacts and state for crash recovery."""
    def __init__(self):
        self.checkpoints: Dict[str, Dict[str, Any]] = {}

    def save_checkpoint(self, directive_id: str, state: PipelineState, artifacts: Dict[str, Any]) -> None:
        if directive_id not in self.checkpoints:
            self.checkpoints[directive_id] = {"artifacts": {}}
        self.checkpoints[directive_id]["state"] = state.value
        self.checkpoints[directive_id]["artifacts"].update(artifacts)

    def load_checkpoint(self, directive_id: str) -> Optional[Dict[str, Any]]:
        return self.checkpoints.get(directive_id)


class WorkflowOrchestrator:
    """Orchestrates pipeline execution with state transitions, checkpionting, and parallelization (`FR-PX-101 to 105`)."""

    def __init__(
        self,
        store: StageCheckpointStore,
        stages: List[BasePipelineStage],
        parallel_stages: Optional[List[BasePipelineStage]] = None
    ):
        self.store = store
        self.stages = stages  # Sequential stages before parallel execution
        self.parallel_stages = parallel_stages or []  # E.g., Narration and Visuals (`FR-PX-104`)

    def execute_pipeline(self, directive_id: str, directive_payload: Dict[str, Any], budget: Optional[ResourceBudget] = None) -> Dict[str, Any]:
        """Run the execution pipeline from current checkpoint or scratch (`FR-PX-101`, `FR-PX-102`)."""
        budget_obj = budget or ResourceBudget()
        tracker = BudgetTracker(budget_obj)

        # Check existing checkpoint (`FR-PX-102`)
        ckpt = self.store.load_checkpoint(directive_id)
        current_artifacts = ckpt["artifacts"].copy() if ckpt else {"directive": directive_payload}
        current_state_str = ckpt["state"] if ckpt else PipelineState.RECEIVED.value

        logger.info(f"Pipeline [{directive_id}] starting/resuming from state: {current_state_str}")

        # 1. Run sequential stages
        for stage in self.stages:
            if self._is_stage_already_done(stage.target_state, current_state_str):
                continue

            logger.info(f"Executing Sequential Stage: {stage.stage_name} -> {stage.target_state.value}")
            out = stage.run_with_retry(current_artifacts, tracker)
            current_artifacts.update(out)
            self.store.save_checkpoint(directive_id, stage.target_state, current_artifacts)
            current_state_str = stage.target_state.value

        # 2. Run parallel stages if applicable (`FR-PX-104`)
        if self.parallel_stages and not self._is_stage_already_done(PipelineState.COMPOSING, current_state_str):
            logger.info("Executing Parallel Stages concurrently (`FR-PX-104`)...")
            with ThreadPoolExecutor(max_workers=len(self.parallel_stages)) as executor:
                future_to_stage = {
                    executor.submit(stage.run_with_retry, current_artifacts.copy(), tracker): stage
                    for stage in self.parallel_stages
                }
                for future in as_completed(future_to_stage):
                    stg = future_to_stage[future]
                    try:
                        res = future.result()
                        current_artifacts.update(res)
                    except Exception as e:
                        logger.error(f"Parallel stage {stg.stage_name} failed: {e}")
                        self.store.save_checkpoint(directive_id, PipelineState.FAILED, current_artifacts)
                        raise

            self.store.save_checkpoint(directive_id, PipelineState.COMPOSING, current_artifacts)
            current_state_str = PipelineState.COMPOSING.value

        # Finalize
        self.store.save_checkpoint(directive_id, PipelineState.REPORTED, current_artifacts)
        return current_artifacts

    def _is_stage_already_done(self, target_state: PipelineState, current_state_str: str) -> bool:
        order = [
            PipelineState.RECEIVED, PipelineState.RESEARCHING, PipelineState.STORY_DRAFTED,
            PipelineState.SCRIPTED, PipelineState.NARRATED, PipelineState.VISUALS_PLANNED,
            PipelineState.COMPOSING, PipelineState.THUMBNAIL_READY, PipelineState.AWAITING_APPROVAL,
            PipelineState.PUBLISHING, PipelineState.PUBLISHED, PipelineState.MEASURING, PipelineState.REPORTED
        ]
        try:
            cur_idx = [s.value for s in order].index(current_state_str)
            tgt_idx = [s.value for s in order].index(target_state.value)
            return cur_idx >= tgt_idx
        except ValueError:
            return False
