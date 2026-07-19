"""
Versioned Prompt Artifact: Lesson Extraction v1 (`FR-PX-1401`, `FR-EC-110`).

Extracts causal learning yield from an experiment `ReflectionReport` and observations.
Enforces strict JSON schema output complying with `Lesson` domain model (`FR-PX-1403`).
"""
from typing import Dict, Any, List
from pydantic import BaseModel, Field


class LessonExtractionPromptMetadata(BaseModel):
    prompt_id: str = "lesson_extraction_v1"
    version: str = "1.0.0"
    task_class: str = "REASONING"
    author: str = "EvolutionOS Core Team"
    description: str = "Extracts validated causal lessons from reflection reports"


PROMPT_TEMPLATE = """
You are the causal learning engine of EvolutionOS.
Analyze the following reflection report and observations from an completed experiment cycle:

Experiment ID: {experiment_id}
Hypothesis Statement: {hypothesis_statement}
Observed Performance Delta: {performance_delta}
Surprise Score: {surprise_score}

Observations Summary:
{observations_summary}

Your task is to formulate formal causal lessons following the strict schema below.
Every lesson MUST explicitly identify the variables involved, the causal direction, and assign an empirical confidence score between 0.01 and 0.99 (`ADR-007`).

Output exactly a JSON object matching this contract (`FR-PX-1403`):
{{
    "lessons": [
        {{
            "statement": "Explicit causal statement relating condition to outcome",
            "confidence": 0.85,
            "applicable_scopes": ["youtube", "education"],
            "supporting_evidence_count": 3
        }}
    ]
}}
"""


def render_prompt(
    experiment_id: str,
    hypothesis_statement: str,
    performance_delta: float,
    surprise_score: float,
    observations_summary: str
) -> str:
    """Render versioned prompt artifact (`FR-PX-1401`)."""
    return PROMPT_TEMPLATE.format(
        experiment_id=experiment_id,
        hypothesis_statement=hypothesis_statement,
        performance_delta=performance_delta,
        surprise_score=surprise_score,
        observations_summary=observations_summary
    )
