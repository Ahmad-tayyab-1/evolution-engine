"""
Pipeline Dry-Run Verification (`Milestone v0.3`, `FR-PX-101` to `FR-PX-1304`).

Verifies:
1. `WorkflowOrchestrator` state machine (`RECEIVED -> ... -> REPORTED`).
2. Checkpointing & crash recovery (`FR-PX-102` / `NFR-AVA-002`).
3. Parallel execution of independent stages (`FR-PX-104`).
4. Resource budget enforcement & halting when limits exceeded (`FR-PX-105`).
5. YouTube adapter publishing and canonical metric normalization (`FR-PX-1001`, `FR-PX-1002`).
6. Multi-provider LLM router task classes, caching, fallback chain, and cost ledger (`FR-PX-1301 to 1304`).
"""
import pytest
from evolutionos.execution.orchestrator.workflow_engine import (
    WorkflowOrchestrator, StageCheckpointStore, PipelineState, ResourceBudget, BudgetExceeded
)
from evolutionos.execution.orchestrator.pipeline_stages.research_stage import ResearchStage
from evolutionos.execution.orchestrator.pipeline_stages.story_stage import StoryStage
from evolutionos.execution.orchestrator.pipeline_stages.script_stage import ScriptStage
from evolutionos.execution.orchestrator.pipeline_stages.narration_stage import NarrationStage
from evolutionos.execution.orchestrator.pipeline_stages.visuals_stage import VisualsStage, CompositionStage
from evolutionos.execution.adapters.youtube.adapter import YouTubePlatformAdapter
from evolutionos.execution.adapters.youtube.metric_mapping import normalize_youtube_metrics
from evolutionos.execution.providers.llm.router import (
    MultiProviderLLMRouter, LLMRequest, TaskClass, CostLedger
)


def test_workflow_orchestrator_full_pipeline_dry_run():
    """Verify end-to-end dry run across all sequential and parallel stages (`FR-PX-101`, `FR-PX-104`)."""
    store = StageCheckpointStore()
    seq_stages = [ResearchStage(), StoryStage(), ScriptStage()]
    parallel_stages = [NarrationStage(), VisualsStage()]

    # We run CompositionStage sequentially after parallel stages complete, or by including it in sequential stages
    # Let's verify we can pass sequential stages before and after parallel, or run a second step
    orchestrator = WorkflowOrchestrator(store=store, stages=seq_stages, parallel_stages=parallel_stages)

    directive = {"topic": "Autonomous AI Evolution", "experiment_id": "exp_v03_1"}
    artifacts = orchestrator.execute_pipeline("directive_101", directive)

    # Check states and outputs
    assert store.load_checkpoint("directive_101")["state"] == PipelineState.REPORTED.value
    assert "fact_ledger" in artifacts
    assert "selected_treatment" in artifacts
    assert "script" in artifacts
    assert "narration_tracks" in artifacts
    assert "visual_assets" in artifacts
    assert len(artifacts["narration_tracks"]) == len(artifacts["script"]["scenes"])


def test_workflow_checkpointing_and_crash_recovery():
    """Verify crash recovery resumes from last checkpoint and skips completed stages (`FR-PX-102`, `NFR-AVA-002`)."""
    store = StageCheckpointStore()
    seq_stages = [ResearchStage(), StoryStage(), ScriptStage()]
    orchestrator = WorkflowOrchestrator(store=store, stages=seq_stages)

    # 1. Run ResearchStage then simulate a crash right after StoryStage
    # We can simulate by saving a checkpoint manually at STORY_DRAFTED
    store.save_checkpoint("directive_102", PipelineState.STORY_DRAFTED, {
        "directive": {"topic": "Crash Recovery Check"},
        "fact_ledger": [{"claim": "Test claim", "verification": "SINGLE_SOURCE"}],
        "selected_treatment": {
            "structure": [{"phase": "Hook", "content": "Welcome after crash recovery!"}],
            "pacing_map": {"0-30s": "HOOK"}
        }
    })

    # 2. Resume execution
    artifacts = orchestrator.execute_pipeline("directive_102", {"topic": "Crash Recovery Check"})

    assert store.load_checkpoint("directive_102")["state"] == PipelineState.REPORTED.value
    assert "script" in artifacts
    assert artifacts["script"]["scenes"][0]["narration_text"] == "Welcome after crash recovery!"


def test_workflow_budget_enforcement():
    """Verify that exceeding ResourceBudget raises BudgetExceeded (`FR-PX-105`)."""
    store = StageCheckpointStore()
    # ResearchStage costs $0.02, StoryStage $0.03, ScriptStage $0.03 -> Total $0.08
    seq_stages = [ResearchStage(), StoryStage(), ScriptStage()]
    orchestrator = WorkflowOrchestrator(store=store, stages=seq_stages)

    # Provide a budget with max_cost_usd = $0.04 (enough for Research ($0.02) + Story ($0.03) -> exceeds!)
    strict_budget = ResourceBudget(max_cost_usd=0.04)

    with pytest.raises(BudgetExceeded) as exc_info:
        orchestrator.execute_pipeline("directive_budget", {"topic": "Budget Limit Test"}, budget=strict_budget)

    assert "Cost limit exceeded" in str(exc_info.value)


def test_youtube_adapter_and_metric_normalization():
    """Verify YouTube adapter dry-run publishing and canonical metric normalization (`FR-PX-1001`, `FR-PX-1002`)."""
    adapter = YouTubePlatformAdapter(dry_run=True)

    pub_res = adapter.publish("memory://render/final_video.mp4", {
        "title": "Normalized Analytics Demo",
        "description": "Testing mapping table",
        "experiment_id": "exp_yt_101"
    })
    assert pub_res["status"] == "PUBLISHED_DRY_RUN"
    assert "yt_dryrun_exp_yt_101" in pub_res["publication_ref"]

    # Collect normalized canonical metrics (`FR-PX-1002`)
    observations = adapter.collect_metrics(pub_res["publication_ref"], window="24h", experiment_id="exp_yt_101")
    metric_map = {obs.metric: obs.value for obs in observations}

    assert "attention_rate" in metric_map
    assert "selection_rate" in metric_map
    assert "audience_growth" in metric_map
    assert "engagement" in metric_map
    assert metric_map["selection_rate"] == 0.085  # 8.5% CTR normalized
    assert metric_map["attention_rate"] == 0.462  # 46.2% retention normalized


def test_llm_router_caching_fallback_and_cost_ledger():
    """Verify multi-provider router task class routing, caching, fallback chain, and cost accounting (`FR-PX-1301 to 1304`)."""
    ledger = CostLedger()
    router = MultiProviderLLMRouter(ledger=ledger)

    # 1. Test Task Class routing & Cost Ledger (`FR-PX-1302`, `FR-PX-1304`)
    req = LLMRequest(
        system_prompt="You are an expert strategist.",
        user_prompt="Analyze optimal topic angles.",
        task_class=TaskClass.REASONING_HEAVY,
        experiment_id="exp_llm_1",
        cacheable=True
    )
    resp1 = router.route_and_execute(req)
    assert resp1.cached is False
    assert resp1.provider_used == "Groq"
    assert resp1.model_used == "llama-3.3-70b-versatile"
    assert ledger.get_experiment_total_cost("exp_llm_1") > 0.0

    # 2. Test Caching (`FR-PX-1303`)
    resp2 = router.route_and_execute(req)
    assert resp2.cached is True
    assert resp2.content == resp1.content
    # Cached hit does not add cost to ledger
    assert len(ledger.entries) == 1

    # 3. Test Fallback chain (`FR-PX-1301`, `NFR-REL-003`)
    # Simulate primary provider failure by temporarily breaking generate method
    original_provider = router.providers["groq_fast"]
    router.providers["groq_fast"] = None  # Force router to skip/fail primary and use fallback

    req_bulk = LLMRequest(
        system_prompt="Write script narration.",
        user_prompt="Scene 1 narration.",
        task_class=TaskClass.GENERATION_BULK,
        experiment_id="exp_llm_2",
        cacheable=False
    )
    resp_fallback = router.route_and_execute(req_bulk)
    assert resp_fallback.provider_used == "OpenAI" or resp_fallback.provider_used == "Local"
    assert ledger.get_experiment_total_cost("exp_llm_2") >= 0.0

    # Restore
    router.providers["groq_fast"] = original_provider
