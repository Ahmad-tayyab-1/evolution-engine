"""
Niche discovery phase.

start_discovery(): call once, before the channel has produced anything.
  - Pre-scans each candidate niche's public view velocity + channel
    concentration as a rough opportunity signal (biases early sampling,
    doesn't decide the winner).
  - Sets StrategyState.phase = 'niche_discovery' with a start/end window.

pick_niche_for_video(): called by ideation.py every video during discovery.
  - Weighted sample across candidates: opportunity_score early on, blended
    with actual own performance (NicheScore) as real data accumulates.
  - Once phase == 'locked', always returns the locked niche.

maybe_conclude_discovery(): called every loop cycle.
  - If the discovery window has elapsed AND every candidate niche has at
    least MIN_VIDEOS_PER_NICHE with metrics, locks the best-performing one.
  - If the window elapsed but data is thin, extends by a short grace period
    instead of locking on noise.
"""
import os
import random
from datetime import datetime, timedelta
from agent.db import get_session, StrategyState, NicheScore, Video
from agent.niches import NICHE_CANDIDATES
from agent import youtube_client as yt

MIN_VIDEOS_PER_NICHE = int(os.getenv("NICHE_MIN_VIDEOS", 2))
GRACE_PERIOD_HOURS = 12


def _view_velocity(view_count: int, published_at: str) -> float:
    published = datetime.strptime(published_at[:19], "%Y-%m-%dT%H:%M:%S")
    days = max((datetime.utcnow() - published).days, 1)
    return view_count / days


def _score_niche_opportunity(niche: str, topics: list) -> float:
    """Higher = more viewer demand relative to how concentrated/saturated the results are."""
    sample_topic = topics[0]
    try:
        videos = yt.search_public_videos(sample_topic, max_results=10, shorts=False)
    except Exception:
        return 0.5  # neutral fallback if search fails

    if not videos:
        return 0.3

    avg_velocity = sum(_view_velocity(v["view_count"], v["published_at"]) for v in videos) / len(videos)
    demand_signal = min(avg_velocity / 1000.0, 5.0)  # normalize, cap outliers
    return round(demand_signal, 3)


def start_discovery(days: int = 3):
    days = max(2, min(days, 5))  # keep within the sane 2-5 day range
    session = get_session()
    state = session.query(StrategyState).first()
    if not state:
        state = StrategyState()
        session.add(state)

    state.phase = "niche_discovery"
    state.discovery_started_at = datetime.utcnow()
    state.discovery_ends_at = datetime.utcnow() + timedelta(days=days)
    session.commit()

    for niche, topics in NICHE_CANDIDATES.items():
        score = _score_niche_opportunity(niche, topics)
        row = session.query(NicheScore).filter_by(niche=niche).first()
        if not row:
            row = NicheScore(niche=niche)
            session.add(row)
        row.opportunity_score = score
        row.updated_at = datetime.utcnow()

    session.commit()
    session.close()


def pick_niche_for_video() -> tuple:
    """Returns (niche_name, topic_pool_list)."""
    session = get_session()
    state = session.query(StrategyState).first()

    if state and state.phase == "locked" and state.locked_niche:
        niche = state.locked_niche
        session.close()
        return niche, NICHE_CANDIDATES[niche]

    scores = session.query(NicheScore).all()
    session.close()

    if not scores:
        niche = random.choice(list(NICHE_CANDIDATES.keys()))
        return niche, NICHE_CANDIDATES[niche]

    # blend opportunity score with actual own performance as it accumulates
    names, weights = [], []
    for s in scores:
        own_signal = (s.avg_ctr * 10 + s.avg_retention / 100) if s.videos_count > 0 else 0
        weight = 0.4 * s.opportunity_score + 0.6 * own_signal + 0.1  # floor so all stay explorable
        names.append(s.niche)
        weights.append(max(weight, 0.05))

    niche = random.choices(names, weights=weights, k=1)[0]
    return niche, NICHE_CANDIDATES.get(niche, list(NICHE_CANDIDATES.values())[0])


def update_niche_performance():
    """Rolls up video metrics into per-niche scores. Call each strategy cycle."""
    session = get_session()
    videos = session.query(Video).filter(
        Video.status == "uploaded", Video.niche.isnot(None), Video.ctr.isnot(None)
    ).all()

    by_niche = {}
    for v in videos:
        by_niche.setdefault(v.niche, []).append(v)

    for niche, vids in by_niche.items():
        row = session.query(NicheScore).filter_by(niche=niche).first()
        if not row:
            row = NicheScore(niche=niche)
            session.add(row)
        row.avg_ctr = sum((v.ctr or 0) for v in vids) / len(vids)
        row.avg_retention = sum((v.avg_view_duration_sec or 0) for v in vids) / len(vids)
        row.videos_count = len(vids)
        row.updated_at = datetime.utcnow()

    session.commit()
    session.close()


def maybe_conclude_discovery():
    session = get_session()
    state = session.query(StrategyState).first()
    if not state or state.phase != "niche_discovery" or not state.discovery_ends_at:
        session.close()
        return

    if datetime.utcnow() < state.discovery_ends_at:
        session.close()
        return  # window still open

    scores = session.query(NicheScore).all()
    thin = [s for s in scores if s.videos_count < MIN_VIDEOS_PER_NICHE]

    if thin and datetime.utcnow() < state.discovery_ends_at + timedelta(hours=GRACE_PERIOD_HOURS):
        # window closed but data is thin - give it a short grace period rather than lock on noise
        session.close()
        return

    if not scores:
        session.close()
        return

    def combined_score(s):
        return s.avg_ctr + s.avg_retention / 1000

    winner = max(scores, key=combined_score)
    state.phase = "locked"
    state.locked_niche = winner.niche
    state.notes = (
        f"Niche discovery concluded: locked '{winner.niche}' "
        f"(avg_ctr={winner.avg_ctr:.4f}, avg_retention={winner.avg_retention:.0f}s, "
        f"n={winner.videos_count})"
    )
    session.commit()
    session.close()
