import random
from agent.db import get_session, TopicScore, StrategyState
from agent.llm import chat_json
from agent import niche_discovery


def _weighted_topic_pick(session, topic_pool: list, active_track: str) -> str:
    rows = session.query(TopicScore).filter(
        TopicScore.format == active_track, TopicScore.topic.in_(topic_pool)
    ).all()
    if not rows:
        return random.choice(topic_pool)
    known = {r.topic for r in rows}
    unknown = [t for t in topic_pool if t not in known]
    topics = [r.topic for r in rows] + unknown
    weights = [r.weight for r in rows] + [0.3] * len(unknown)
    return random.choices(topics, weights=weights, k=1)[0]


def generate_video_idea(genome) -> dict:
    """Returns {title, topic, niche, format, hook, outline}. genome supplies the system prompt."""
    session = get_session()
    state = session.query(StrategyState).first()
    active_track = state.active_track if state else "long"

    niche, topic_pool = niche_discovery.pick_niche_for_video()
    seed = _weighted_topic_pick(session, topic_pool, active_track)
    session.close()

    length_note = (
        genome.length_note_shorts if active_track == "shorts" else genome.length_note_long
    )

    idea = chat_json(
        system=genome.ideation_system_prompt,
        user=(
            f"Seed theme: {seed}\n"
            f"Target format: {active_track} ({length_note})\n"
            "Make the title curiosity-driven but not clickbait-false. "
            "Avoid copyrighted characters/franchises/brand names."
        ),
    )
    idea["format"] = active_track
    idea["niche"] = niche
    return idea
