"""
Channel branding SEO - description + keywords only. Profile picture, banner,
and channel name stay manual by design.

apply_initial_branding(): called once when niche discovery locks in.
maybe_refresh_branding(): called periodically after that, so the
  description/keywords can incorporate what's actually performing well -
  same spirit as genome evolution but scoped to channel-level metadata.
"""
import os
from datetime import datetime, timedelta
from agent.db import get_session, StrategyState, TopicScore, Video
from agent.llm import chat_json
from agent import youtube_client as yt

REFRESH_EVERY_DAYS = int(os.getenv("BRANDING_REFRESH_DAYS", 14))


def _top_topics_text(session, niche_topics: list, limit: int = 5) -> str:
    rows = (
        session.query(TopicScore)
        .filter(TopicScore.topic.in_(niche_topics))
        .order_by(TopicScore.weight.desc())
        .limit(limit)
        .all()
    )
    if not rows:
        return ", ".join(niche_topics[:limit])
    return ", ".join(r.topic for r in rows)


def _generate_branding(niche: str, topics_text: str, channel_title: str) -> dict:
    return chat_json(
        system=(
            "You write YouTube channel-level branding metadata (not video metadata). "
            "Respond ONLY as JSON: {\"description\": str, \"keywords\": str}. "
            "description: 3-4 sentences, tells a new visitor exactly what the channel "
            "covers and why to subscribe, no video-specific details, no emoji spam, "
            "professional but inviting tone. "
            "keywords: a single space-separated string in YouTube's expected format - "
            "wrap multi-word phrases in double quotes, e.g. "
            "'\"space facts\" \"ancient history\" science education'. 12-18 total terms/"
            "phrases covering the niche broadly, not just current topics."
        ),
        user=(
            f"Channel name: {channel_title}\n"
            f"Niche: {niche.replace('_', ' ')}\n"
            f"Best-performing topics so far: {topics_text}"
        ),
        temperature=0.5,
    )


def _apply(niche: str):
    session = get_session()
    from agent.niches import NICHE_CANDIDATES
    topics_text = _top_topics_text(session, NICHE_CANDIDATES.get(niche, []))
    session.close()

    current = yt.get_channel_branding()
    result = _generate_branding(niche, topics_text, current["title"])
    yt.update_channel_branding(description=result["description"], keywords=result["keywords"])

    session = get_session()
    state = session.query(StrategyState).first()
    state.branding_last_applied_at = datetime.utcnow()
    session.commit()
    session.close()


def apply_initial_branding():
    session = get_session()
    state = session.query(StrategyState).first()
    if not state or not state.locked_niche or state.branding_last_applied_at:
        session.close()
        return  # not locked yet, or already applied once
    niche = state.locked_niche
    session.close()
    _apply(niche)


def maybe_refresh_branding():
    """Periodically re-generates description/keywords from latest top-performing topics."""
    session = get_session()
    state = session.query(StrategyState).first()
    if not state or state.phase != "locked" or not state.locked_niche:
        session.close()
        return
    if not state.branding_last_applied_at:
        session.close()
        return  # initial branding hasn't run yet

    due = datetime.utcnow() - state.branding_last_applied_at >= timedelta(days=REFRESH_EVERY_DAYS)
    niche = state.locked_niche
    session.close()

    if due:
        _apply(niche)
