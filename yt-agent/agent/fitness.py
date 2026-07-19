"""
Fitness Function & Analytics Collector helper.

Implements Module 8 (Fitness Function) & Module 2 (Analytics Collector) from Evolution_Engine_Plan.md.
Calculates weighted fitness:
Fitness = 30% CTR + 35% Retention + 20% Watch Time + 10% Subscribers + 5% Comments
"""
from datetime import datetime
from agent.db import get_session, Video, AnalyticsSnapshot
from agent import youtube_client as yt


# Default fitness weights (can also evolve over time)
WEIGHT_CTR = 0.30
WEIGHT_RETENTION = 0.35
WEIGHT_WATCH_TIME = 0.20
WEIGHT_SUBS = 0.10
WEIGHT_COMMENTS = 0.05


def calculate_fitness_score(ctr: float, retention_pct: float, watch_time_hours: float, subs_gained: int, comments: int) -> float:
    """
    Normalized calculation where each component contributes toward an overall fitness score (target 0.0 to 1.0+).
    """
    # Normalize metrics to [0, 1] relative targets:
    # Target CTR: 10% (0.10)
    norm_ctr = min((ctr or 0.0) / 0.10, 1.5)
    # Target Retention: 60% (60.0)
    norm_ret = min((retention_pct or 0.0) / 60.0, 1.5)
    # Target Watch Time per batch/video: 5 hours
    norm_watch = min((watch_time_hours or 0.0) / 5.0, 1.5)
    # Target Subs gained per video: 10
    norm_subs = min((subs_gained or 0) / 10.0, 1.5)
    # Target Comments per video: 5
    norm_comments = min((comments or 0) / 5.0, 1.5)

    fitness = (
        WEIGHT_CTR * norm_ctr +
        WEIGHT_RETENTION * norm_ret +
        WEIGHT_WATCH_TIME * norm_watch +
        WEIGHT_SUBS * norm_subs +
        WEIGHT_COMMENTS * norm_comments
    )
    return round(fitness, 4)


def collect_and_score_video(video_id: int) -> float:
    """
    Fetches latest YouTube stats for a video, creates an AnalyticsSnapshot,
    computes and stores its fitness score.
    """
    session = get_session()
    v = session.query(Video).filter_by(id=video_id).first()
    if not v or not v.youtube_id:
        session.close()
        return 0.0

    try:
        metrics = yt.get_video_metrics(v.youtube_id)
        views = metrics.get("views", 0)
        likes = metrics.get("likes", 0)
        ctr = metrics.get("ctr", 0.0)
        avg_dur = metrics.get("avg_view_duration_sec", 0.0)
        
        # Approximate retention % assuming 10 min average or format-specific duration
        duration_total = 60.0 if v.format == "shorts" else 600.0
        retention_pct = min((avg_dur / duration_total) * 100.0, 100.0) if duration_total else 0.0
        subs_gained = metrics.get("subs_gained", 0)
        comments = metrics.get("comments", 0)
        shares = metrics.get("shares", 0)
        watch_minutes = metrics.get("watch_minutes", 0)
        watch_time_hours = watch_minutes / 60.0 if watch_minutes else (views * avg_dur) / 3600.0

        # Create snapshot
        fitness = calculate_fitness_score(
            ctr=ctr,
            retention_pct=retention_pct,
            watch_time_hours=watch_time_hours,
            subs_gained=subs_gained,
            comments=comments
        )

        v.views = views
        v.likes = likes
        v.ctr = ctr
        v.avg_view_duration_sec = avg_dur
        v.fitness = fitness

        snap = AnalyticsSnapshot(
            video_id=v.id,
            youtube_id=v.youtube_id,
            ctr=ctr,
            views=views,
            watch_time_hours=watch_time_hours,
            avg_view_duration_sec=avg_dur,
            retention_pct=retention_pct,
            subscribers_gained=subs_gained,
            likes=likes,
            comments=comments,
            shares=shares,
            fitness_score=fitness,
            snapshot_at=datetime.utcnow()
        )
        session.add(snap)
        session.commit()
        session.close()
        return fitness
    except Exception as e:
        session.close()
        raise e
