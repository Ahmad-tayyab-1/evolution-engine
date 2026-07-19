"""
Strategy engine.

Every loop cycle:
1. Pull fresh channel-level + video-level analytics.
2. Update per-topic performance scores (topic_scores table).
3. Update StrategyState (subs / watch hours / shorts views) against the
   monetization goal, and decide which track (long vs shorts) to lean into.
4. Recompute sampling weights ideation.py uses to pick the next topic.
"""
import os
from datetime import datetime
from agent.db import get_session, TopicScore, Video, StrategyState
from agent import youtube_client as yt

GOAL_SUBS = int(os.getenv("GOAL_SUBS", 1000))
GOAL_WATCH_HOURS = float(os.getenv("GOAL_WATCH_HOURS", 4000))
GOAL_SHORTS_VIEWS_90D = int(os.getenv("GOAL_SHORTS_VIEWS_90D", 10_000_000))


def _get_or_create_state(session) -> StrategyState:
    state = session.query(StrategyState).first()
    if not state:
        state = StrategyState()
        session.add(state)
        session.commit()
    return state


def refresh_channel_progress():
    """Pull channel-level stats and update progress toward monetization."""
    session = get_session()
    state = _get_or_create_state(session)

    stats = yt.get_channel_stats()  # {"subs":.., "watch_hours_12mo":.., "shorts_views_90d":..}
    state.subs = stats["subs"]
    state.watch_hours_12mo = stats["watch_hours_12mo"]
    state.shorts_views_90d = stats["shorts_views_90d"]
    state.last_evaluated_at = datetime.utcnow()

    # Decide which track is closer to unlocking monetization
    long_progress = min(state.subs / GOAL_SUBS, state.watch_hours_12mo / GOAL_WATCH_HOURS)
    shorts_progress = min(state.subs / GOAL_SUBS, state.shorts_views_90d / GOAL_SHORTS_VIEWS_90D)
    state.active_track = "shorts" if shorts_progress >= long_progress else "long"

    state.notes = (
        f"long_progress={long_progress:.2%} shorts_progress={shorts_progress:.2%} "
        f"-> leaning {state.active_track}"
    )
    session.commit()
    session.close()
    return state


def update_topic_scores():
    """Pull per-video analytics for recently published videos and re-score topics."""
    session = get_session()
    videos = session.query(Video).filter(Video.status == "uploaded").all()

    for v in videos:
        if not v.youtube_id:
            continue
        metrics = yt.get_video_metrics(v.youtube_id)  # ctr, avg_view_duration_sec, views, likes
        v.views = metrics["views"]
        v.likes = metrics["likes"]
        v.ctr = metrics["ctr"]
        v.avg_view_duration_sec = metrics["avg_view_duration_sec"]

        topic_row = session.query(TopicScore).filter_by(topic=v.topic, format=v.format).first()
        if not topic_row:
            topic_row = TopicScore(topic=v.topic, format=v.format)
            session.add(topic_row)

        n = topic_row.videos_count or 0
        # running average update (guard against None)
        prev_ctr = topic_row.avg_ctr or 0.0
        prev_ret = topic_row.avg_retention or 0.0
        topic_row.avg_ctr = (prev_ctr * n + (v.ctr or 0)) / (n + 1)
        topic_row.avg_retention = (
            prev_ret * n + (v.avg_view_duration_sec or 0)
        ) / (n + 1)
        topic_row.avg_view_duration_sec = topic_row.avg_retention
        topic_row.videos_count = n + 1
        topic_row.updated_at = datetime.utcnow()

    session.commit()
    _recompute_weights(session)
    session.close()


def _recompute_weights(session):
    """Higher CTR + retention => higher sampling weight for future ideation."""
    rows = session.query(TopicScore).all()
    if not rows:
        return
    max_ctr = max((r.avg_ctr for r in rows), default=1) or 1
    max_ret = max((r.avg_retention for r in rows), default=1) or 1
    for r in rows:
        norm_ctr = (r.avg_ctr / max_ctr) if max_ctr else 0
        norm_ret = (r.avg_retention / max_ret) if max_ret else 0
        # base weight of 0.3 so untested/new topics still get explored
        r.weight = round(0.3 + 0.7 * (0.5 * norm_ctr + 0.5 * norm_ret), 3)
    session.commit()


def generate_active_strategy(session, active_track: str):
    """
    Module 5 (Strategy Engine): Reads the Knowledge Base before every production cycle,
    produces a concrete strategy plan with risk level and mutation direction.
    """
    from agent.db import Rule, Strategy, CompetitorInsight
    from agent.llm import chat_json

    rules = session.query(Rule).all()
    rules_text = "\n".join([f"- [{r.category}] (conf {r.confidence}): {r.rule}" for r in rules])
    
    recent_insights = session.query(CompetitorInsight).order_by(CompetitorInsight.scraped_at.desc()).limit(3).all()
    insights_text = "\n".join([f"- ({i.topic}): {i.summary}" for i in recent_insights])

    prompt = (
        "You are the Strategy Engine of an evolutionary YouTube intelligence system. "
        "Before generating our next video, formulate a strategic direction based on our accumulated Knowledge Base.\n"
        f"Active Track (Format Focus): {active_track}\n"
        f"KNOWLEDGE BASE RULES:\n{rules_text}\n\n"
        f"RECENT COMPETITOR INSIGHTS:\n{insights_text}\n\n"
        "Output ONLY JSON with keys:\n"
        "{\n"
        '  "summary": str (1-2 sentences summarizing content direction),\n'
        '  "reasoning": str (why this strategy leverages our top rules),\n'
        '  "mutation_plan": str (what types of variations we should test next),\n'
        '  "risk_level": "low" | "moderate" | "high"\n'
        "}"
    )

    try:
        data = chat_json(
            system="You formulate data-driven content strategies combining rules and market signals.",
            user=prompt,
            temperature=0.7
        )
        strat = Strategy(
            summary=data.get("summary", f"Focusing on high-retention {active_track} mystery stories."),
            reasoning=data.get("reasoning", "Leveraging highest-confidence hook and thumbnail rules."),
            mutation_plan=data.get("mutation_plan", "Testing title formulas vs hook structures."),
            risk_level=data.get("risk_level", "moderate")
        )
        session.add(strat)
        session.commit()
        return strat
    except Exception:
        strat = Strategy(
            summary=f"Executing baseline optimized {active_track} mystery production.",
            reasoning="Applying confirmed knowledge base principles for CTR and retention.",
            mutation_plan="Single-variable hook and pacing testing.",
            risk_level="moderate"
        )
        session.add(strat)
        session.commit()
        return strat


def run_full_cycle():
    state = refresh_channel_progress()
    update_topic_scores()
    
    session = get_session()
    strat = generate_active_strategy(session, state.active_track)
    session.close()
    return state, strat

