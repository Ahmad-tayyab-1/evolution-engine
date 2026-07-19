"""
Experiment Engine.

Implements Module 4 (Experiment Engine) from Evolution_Engine_Plan.md.
Every upload should intentionally test one or two variables only (e.g., Hook type, Thumbnail color,
Title style, Script length, Voice speed, Publish time). Never mutates everything at once.
"""
from datetime import datetime
from agent.db import get_session, Experiment, Rule, Genome
from agent.llm import chat_json


def formulate_experiment(genome: Genome, video_id: int, format_type: str) -> int:
    """
    Selects a single variable to mutate based on the current Knowledge Base confidence gaps,
    creates an Experiment record, and returns the experiment_id.
    """
    session = get_session()
    rules = session.query(Rule).order_by(Rule.confidence.asc()).all()
    rules_context = "\n".join([f"- ({r.category}) [conf={r.confidence}]: {r.rule}" for r in rules])

    prompt = (
        "You are the Experiment Engine of an evolutionary YouTube intelligence system. "
        "Select exactly ONE single variable to test for our next video upload to isolate cause and effect.\n"
        f"Video Format: {format_type}\n"
        f"Current Genome Version: {genome.version}\n"
        f"KNOWLEDGE BASE (Lower confidence rules need testing):\n{rules_context}\n\n"
        "Choose ONE variable from: hook_type, title_structure, thumbnail_style, scene_pacing, visual_mood.\n"
        "Respond ONLY as JSON:\n"
        "{\n"
        '  "variable": str,\n'
        '  "old_value": str (current control state),\n'
        '  "new_value": str (the specific single mutation being applied),\n'
        '  "hypothesis": str (e.g. "Changing X to Y will increase CTR by isolating..."),\n'
        '  "prompt_injection": str (specific instruction to inject into candidate/script generation for this test)\n'
        "}"
    )

    try:
        data = chat_json(
            system="You design rigorous, single-variable scientific tests for content generation.",
            user=prompt,
            temperature=0.7
        )
        exp = Experiment(
            video_id=video_id,
            variable=data.get("variable", "hook_type"),
            old_value=data.get("old_value", "control standard"),
            new_value=data.get("new_value", "mutated test variant"),
            hypothesis=data.get("hypothesis", "Testing impact of mutation on retention/CTR."),
            result="pending",
            created_at=datetime.utcnow()
        )
        session.add(exp)
        session.commit()
        exp_id = exp.id
        session.close()
        return exp_id, data.get("prompt_injection", "")
    except Exception:
        # Default safety fallback experiment
        exp = Experiment(
            video_id=video_id,
            variable="hook_type",
            old_value="Standard introductory hook",
            new_value="High-stakes mystery contradiction hook",
            hypothesis="Opening with a direct contradiction increases first-30-second retention.",
            result="pending",
            created_at=datetime.utcnow()
        )
        session.add(exp)
        session.commit()
        exp_id = exp.id
        session.close()
        return exp_id, "CRITICAL TEST: Open the script narration with an immediate, shocking high-stakes contradiction without any warmup."
