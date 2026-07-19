"""
Learning Engine & Knowledge Base updater.

Implements Module 3 (Learning Engine) & Module 1 (Knowledge Base updates) from Evolution_Engine_Plan.md.
For every evaluated upload/experiment, answers:
- Why did it perform?
- What improved or worsened?
- Was the tested hypothesis confirmed?
Outputs structured lessons with confidence scores that update the durable Knowledge Base.
"""
from datetime import datetime
from agent.db import get_session, Video, Rule, Experiment, AnalyticsSnapshot
from agent.llm import chat_json


def evaluate_experiment_and_learn(video_id: int):
    """
    Evaluates a video after it has accumulated analytics/fitness score,
    determines if its experiment hypothesis was confirmed/refuted, and updates the Knowledge Base.
    """
    session = get_session()
    v = session.query(Video).filter_by(id=video_id).first()
    if not v or not v.experiment_id:
        session.close()
        return

    exp = session.query(Experiment).filter_by(id=v.experiment_id).first()
    if not exp or exp.result != "pending":
        session.close()
        return

    # Compare against channel/control averages
    control_videos = session.query(Video).filter(
        Video.id != video_id,
        Video.status == "uploaded",
        Video.fitness.isnot(None)
    ).order_by(Video.created_at.desc()).limit(10).all()

    avg_control_fitness = sum(cv.fitness for cv in control_videos) / len(control_videos) if control_videos else 0.5
    avg_control_ctr = sum(cv.ctr or 0 for cv in control_videos) / len(control_videos) if control_videos else 0.05

    # Determine hypothesis outcome
    confirmed = v.fitness > (avg_control_fitness * 1.08)  # 8% better than control
    refuted = v.fitness < (avg_control_fitness * 0.92)
    
    if confirmed:
        exp.result = "confirmed"
    elif refuted:
        exp.result = "refuted"
    else:
        exp.result = "inconclusive"
    exp.evaluated_at = datetime.utcnow()

    # Ask LLM to synthesize a durable rule
    existing_rules = session.query(Rule).all()
    rules_text = "\n".join([f"[{r.id}] ({r.category}, conf={r.confidence}): {r.rule}" for r in existing_rules])

    prompt = (
        "You are the Learning Engine of an autonomous YouTube evolution system. "
        "Analyze the result of a single-variable experiment and extract a durable knowledge rule.\n"
        f"Experiment Variable: {exp.variable}\n"
        f"Old Value: {exp.old_value}\n"
        f"New Value: {exp.new_value}\n"
        f"Hypothesis: {exp.hypothesis}\n"
        f"Outcome: {exp.result.upper()} (Video Fitness: {v.fitness:.4f} vs Baseline: {avg_control_fitness:.4f}, Video CTR: {v.ctr:.3f} vs Baseline: {avg_control_ctr:.3f})\n\n"
        f"EXISTING KNOWLEDGE BASE RULES:\n{rules_text}\n\n"
        "If confirmed or refuted, output ONE structured rule update. Respond ONLY as JSON:\n"
        "{\n"
        '  "action": "new_rule" | "update_rule" | "none",\n'
        '  "rule_id": int | null (if update_rule),\n'
        '  "rule_text": str (concise, actionable principle without fluff),\n'
        '  "category": "hook" | "title" | "thumbnail" | "pacing" | "topic" | "general",\n'
        '  "confidence_delta": float (-0.2 to +0.2 change or initial confidence 0.6 to 0.8),\n'
        '  "reasoning": str\n'
        "}"
    )

    try:
        lesson = chat_json(system="You are an expert data-driven content scientist.", user=prompt, temperature=0.5)
        action = lesson.get("action")
        if action == "new_rule" and lesson.get("rule_text"):
            new_r = Rule(
                rule=lesson["rule_text"],
                category=lesson.get("category", "general"),
                confidence=min(max(lesson.get("confidence_delta", 0.65), 0.1), 1.0),
                evidence_count=1,
                metrics_impacted=exp.variable,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(new_r)
        elif action == "update_rule" and lesson.get("rule_id"):
            target_r = session.query(Rule).filter_by(id=lesson["rule_id"]).first()
            if target_r:
                target_r.confidence = min(max(target_r.confidence + lesson.get("confidence_delta", 0.1), 0.1), 1.0)
                target_r.evidence_count += 1
                target_r.updated_at = datetime.utcnow()
                if lesson.get("rule_text") and len(lesson["rule_text"]) > 10:
                    target_r.rule = lesson["rule_text"]
    except Exception as e:
        pass  # keep learning resilient even if LLM output fails

    session.commit()
    session.close()
