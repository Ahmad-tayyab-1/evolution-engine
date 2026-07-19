"""
Scans public YouTube search results for top-performing videos in the
channel's active topics, and asks the LLM to synthesize what's working
(title patterns, hooks, pacing signals, thumbnail style) as competitive
intel to feed into genome mutation.

Uses only public YouTube Data API search/videos endpoints - no access to
competitor channels' private analytics, just what's publicly visible
(view counts, titles, descriptions, tags, duration, publish date).
"""
from datetime import datetime, timedelta
from agent.db import get_session, TopicScore, CompetitorInsight
from agent.llm import chat_json
from agent import youtube_client as yt


def _view_velocity(view_count: int, published_at: str) -> float:
    published = datetime.strptime(published_at[:19], "%Y-%m-%dT%H:%M:%S")
    days = max((datetime.utcnow() - published).days, 1)
    return view_count / days


def scan_topic(topic: str, fmt: str, max_results: int = 8) -> dict:
    """Finds high-velocity public videos for a topic, summarizes patterns."""
    candidates = yt.search_public_videos(topic, max_results=max_results, shorts=(fmt == "shorts"))
    if not candidates:
        return None

    ranked = sorted(candidates, key=lambda v: _view_velocity(v["view_count"], v["published_at"]), reverse=True)
    top = ranked[: min(5, len(ranked))]

    evidence = "\n".join(
        f"- \"{v['title']}\" | {v['view_count']:,} views | {v['duration_sec']}s | "
        f"tags: {', '.join(v['tags'][:6])}"
        for v in top
    )

    result = chat_json(
        system=(
            "You are a YouTube competitive analyst. Given a list of currently high-velocity "
            "public videos in a topic, identify the recurring patterns that likely drive "
            "performance: title structure/wording, hook style, pacing (duration), thumbnail "
            "style implied by the title, and tag patterns. Respond ONLY as JSON: "
            "{\"summary\": str} - a concise, actionable paragraph a content creator could "
            "apply to their own videos. Do not quote titles verbatim beyond a few words."
        ),
        user=f"Topic: {topic} ({fmt})\nTop videos by view velocity:\n{evidence}",
        temperature=0.4,
    )

    session = get_session()
    row = CompetitorInsight(
        topic=topic, format=fmt, summary=result["summary"],
        source_video_ids=",".join(v["video_id"] for v in top),
    )
    session.add(row)
    session.commit()
    session.close()
    return result


def scan_active_topics(limit_topics: int = 3) -> list:
    """Scans the top-weighted topics the strategy engine currently favors."""
    session = get_session()
    topics = (
        session.query(TopicScore)
        .order_by(TopicScore.weight.desc())
        .limit(limit_topics)
        .all()
    )
    topics = [(t.topic, t.format) for t in topics]
    session.close()

    insights = []
    for topic, fmt in topics:
        insight = scan_topic(topic, fmt)
        if insight:
            insights.append({"topic": topic, "format": fmt, "summary": insight["summary"]})
    return insights


def recent_insights_text(max_age_days: int = 7, limit: int = 5) -> str:
    """Pulls recent competitor insights as a text blob for genome mutation prompts."""
    session = get_session()
    cutoff = datetime.utcnow() - timedelta(days=max_age_days)
    rows = (
        session.query(CompetitorInsight)
        .filter(CompetitorInsight.scraped_at >= cutoff)
        .order_by(CompetitorInsight.scraped_at.desc())
        .limit(limit)
        .all()
    )
    session.close()
    if not rows:
        return "No recent competitor data available yet."
    return "\n".join(f"- [{r.topic}/{r.format}] {r.summary}" for r in rows)
