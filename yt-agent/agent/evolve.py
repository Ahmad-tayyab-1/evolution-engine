"""
Self-evolution engine.

Cycle (run every N hours, not every loop tick - needs data to accumulate):
1. Gather own top/bottom performing videos under the current control genome.
2. Gather competitor/viral insights for active topics.
3. Ask the LLM to propose ONE mutated genome (prompt tweaks + pacing tweaks)
   with a stated rationale.
4. Save it as a 'candidate' genome. loop.py alternates control/candidate
   across new videos.
5. Once a candidate has enough uploaded videos with metrics, compare its
   avg CTR/retention against the control cohort from the same window.
   Promote if meaningfully better, retire if not.
"""
import os
from datetime import datetime
from agent.db import get_session, Genome, Video
from agent.llm import chat_json
from agent import competitor_scan

MIN_SAMPLE_SIZE = int(os.getenv("EVOLVE_MIN_SAMPLE", 4))
IMPROVEMENT_MARGIN = float(os.getenv("EVOLVE_IMPROVEMENT_MARGIN", 0.10))  # 10% better to win


def _get_control(session) -> Genome:
    return session.query(Genome).filter_by(status="control").first()


def _own_performance_summary(session, genome_version: int, limit: int = 10) -> str:
    videos = (
        session.query(Video)
        .filter(Video.genome_version == genome_version, Video.status == "uploaded", Video.ctr.isnot(None))
        .order_by(Video.ctr.desc())
        .limit(limit)
        .all()
    )
    if not videos:
        return "No performance data yet for this genome."
    lines = [
        f"- \"{v.title}\" | ctr={v.ctr:.3f} | avg_view_duration={v.avg_view_duration_sec or 0:.0f}s | topic={v.topic}"
        for v in videos
    ]
    return "\n".join(lines)


def propose_mutation() -> Genome:
    session = get_session()
    control = _get_control(session)
    if not control:
        session.close()
        return None

    own_perf = _own_performance_summary(session, control.version)
    competitor_text = competitor_scan.recent_insights_text()

    mutation = chat_json(
        system=(
            "You are optimizing a YouTube content-generation system. You will propose ONE "
            "concrete mutation to the current 'genome' (prompt templates + pacing params) to "
            "try to improve performance (CTR, retention). Base your proposal on the channel's "
            "own past performance AND on competitor/viral patterns provided. Make ONE clear, "
            "testable change at a time (e.g. punchier hooks, shorter scenes, different title "
            "structure, more scenes for long-form) - not a total rewrite. "
            "Respond ONLY as JSON with keys: "
            "ideation_system_prompt, script_system_prompt, seo_system_prompt, "
            "thumbnail_style_prompt, scene_count_long, scene_count_shorts, "
            "length_note_long, length_note_shorts, rationale (1-2 sentences explaining "
            "the single change you made and why)."
        ),
        user=(
            f"CURRENT GENOME (control, version {control.version}):\n"
            f"ideation_system_prompt: {control.ideation_system_prompt}\n"
            f"script_system_prompt: {control.script_system_prompt}\n"
            f"seo_system_prompt: {control.seo_system_prompt}\n"
            f"thumbnail_style_prompt: {control.thumbnail_style_prompt}\n"
            f"scene_count_long: {control.scene_count_long}, scene_count_shorts: {control.scene_count_shorts}\n"
            f"length_note_long: {control.length_note_long}, length_note_shorts: {control.length_note_shorts}\n\n"
            f"OWN TOP-PERFORMING VIDEOS UNDER THIS GENOME:\n{own_perf}\n\n"
            f"COMPETITOR/VIRAL PATTERNS IN ACTIVE TOPICS:\n{competitor_text}\n\n"
            "Propose the mutated genome now."
        ),
        temperature=0.8,
    )

    next_version = session.query(Genome).count() + 1
    candidate = Genome(
        version=next_version,
        status="candidate",
        parent_version=control.version,
        ideation_system_prompt=mutation["ideation_system_prompt"],
        script_system_prompt=mutation["script_system_prompt"],
        seo_system_prompt=mutation["seo_system_prompt"],
        thumbnail_style_prompt=mutation["thumbnail_style_prompt"],
        scene_count_long=int(mutation["scene_count_long"]),
        scene_count_shorts=int(mutation["scene_count_shorts"]),
        length_note_long=mutation["length_note_long"],
        length_note_shorts=mutation["length_note_shorts"],
        mutation_rationale=mutation["rationale"],
    )
    session.add(candidate)
    session.commit()
    result = candidate
    session.close()
    return result


def _avg_metrics(session, genome_version: int):
    videos = (
        session.query(Video)
        .filter(Video.genome_version == genome_version, Video.status == "uploaded", Video.ctr.isnot(None))
        .all()
    )
    if len(videos) < MIN_SAMPLE_SIZE:
        return None, len(videos)
    avg_ctr = sum(v.ctr for v in videos) / len(videos)
    avg_ret = sum((v.avg_view_duration_sec or 0) for v in videos) / len(videos)
    return {"avg_ctr": avg_ctr, "avg_retention": avg_ret}, len(videos)


def evaluate_candidates():
    """Promotes a candidate to control if it beats control by IMPROVEMENT_MARGIN, else retires it."""
    session = get_session()
    control = _get_control(session)
    candidates = session.query(Genome).filter_by(status="candidate").all()

    control_metrics, control_n = _avg_metrics(session, control.version) if control else (None, 0)

    for cand in candidates:
        cand_metrics, cand_n = _avg_metrics(session, cand.version)
        if not cand_metrics:
            continue  # not enough data yet, leave running

        cand.avg_ctr = cand_metrics["avg_ctr"]
        cand.avg_retention = cand_metrics["avg_retention"]
        cand.videos_produced = cand_n

        if not control_metrics:
            # no control baseline yet, promote candidate by default once it has data
            _promote(session, cand, control)
            continue

        # combined score: CTR and retention both matter
        cand_score = cand_metrics["avg_ctr"] + cand_metrics["avg_retention"] / 1000
        control_score = control_metrics["avg_ctr"] + control_metrics["avg_retention"] / 1000

        if control_score == 0 or (cand_score - control_score) / max(control_score, 1e-6) >= IMPROVEMENT_MARGIN:
            _promote(session, cand, control)
        elif (control_score - cand_score) / max(control_score, 1e-6) >= IMPROVEMENT_MARGIN:
            cand.status = "retired"
            cand.retired_at = datetime.utcnow()

    session.commit()
    session.close()


def _promote(session, candidate: Genome, old_control: Genome):
    candidate.status = "control"
    candidate.promoted_at = datetime.utcnow()
    if old_control:
        old_control.status = "retired"
        old_control.retired_at = datetime.utcnow()


def run_evolution_cycle():
    """Full cycle: score recent videos, learn from experiments, scan competitors, evaluate candidate genomes, maybe propose new mutation."""
    from agent.fitness import collect_and_score_video
    from agent.learning import evaluate_experiment_and_learn

    session = get_session()
    # 1. Collect analytics & calculate fitness for recent uploaded videos
    recent_videos = session.query(Video).filter(Video.status == "uploaded").order_by(Video.published_at.desc()).limit(20).all()
    video_ids = [v.id for v in recent_videos]
    session.close()

    for vid_id in video_ids:
        try:
            collect_and_score_video(vid_id)
            evaluate_experiment_and_learn(vid_id)
        except Exception:
            pass

    session = get_session()
    active_candidates = session.query(Genome).filter_by(status="candidate").count()
    session.close()

    competitor_scan.scan_active_topics(limit_topics=3)
    evaluate_candidates()

    # keep at most 1 candidate running at a time to keep A/B comparisons clean
    if active_candidates == 0:
        propose_mutation()

