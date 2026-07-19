"""
Switchable DB backend (sqlite / postgresql / mysql) driven by env vars,
same pattern as DocuLearn.
"""
import os
from datetime import datetime
from sqlalchemy import (
    create_engine, Column, Integer, String, Float, DateTime, Text, Boolean
)
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


def _build_db_url() -> str:
    backend = os.getenv("DB_BACKEND", "sqlite").lower()
    if backend == "sqlite":
        path = os.getenv("DB_PATH", "./db/agent.db")
        return f"sqlite:///{path}"
    if backend == "postgresql":
        return (
            f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
            f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME')}"
        )
    if backend == "mysql":
        return (
            f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
            f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME')}"
        )
    raise ValueError(f"Unsupported DB_BACKEND: {backend}")


engine = create_engine(_build_db_url(), future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, future=True)


class TopicScore(Base):
    """Strategy engine's memory of what performs well."""
    __tablename__ = "topic_scores"
    id = Column(Integer, primary_key=True)
    topic = Column(String(255), unique=True, nullable=False)
    format = Column(String(20), default="short")  # short | long
    avg_ctr = Column(Float, default=0.0)
    avg_retention = Column(Float, default=0.0)
    avg_view_duration_sec = Column(Float, default=0.0)
    videos_count = Column(Integer, default=0)
    weight = Column(Float, default=1.0)  # sampling weight for ideation
    updated_at = Column(DateTime, default=datetime.utcnow)


class Video(Base):
    __tablename__ = "videos"
    id = Column(Integer, primary_key=True)
    youtube_id = Column(String(64), nullable=True)
    title = Column(String(255))
    topic = Column(String(255))
    format = Column(String(20))  # short | long
    status = Column(String(30), default="planned")
    # planned -> scripted -> assets_ready -> assembled -> uploaded -> failed
    script_path = Column(Text, nullable=True)
    video_path = Column(Text, nullable=True)
    thumbnail_path = Column(Text, nullable=True)
    published_at = Column(DateTime, nullable=True)
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    ctr = Column(Float, nullable=True)
    avg_view_duration_sec = Column(Float, nullable=True)
    genome_version = Column(Integer, nullable=True)  # which genome produced this video
    niche = Column(String(100), nullable=True)  # which candidate niche this video belongs to
    strategy_id = Column(Integer, nullable=True)
    experiment_id = Column(Integer, nullable=True)
    fitness = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)


class NicheScore(Base):
    """Aggregate performance per candidate niche during/after discovery."""
    __tablename__ = "niche_scores"
    id = Column(Integer, primary_key=True)
    niche = Column(String(100), unique=True, nullable=False)
    opportunity_score = Column(Float, default=0.0)  # pre-scan market signal, discovery start only
    avg_ctr = Column(Float, default=0.0)
    avg_retention = Column(Float, default=0.0)
    videos_count = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow)


class CommentQueue(Base):
    __tablename__ = "comment_queue"
    id = Column(Integer, primary_key=True)
    youtube_comment_id = Column(String(64))
    video_youtube_id = Column(String(64))
    author = Column(String(255))
    text = Column(Text)
    draft_reply = Column(Text, nullable=True)
    status = Column(String(20), default="pending")  # pending | approved | posted | rejected
    created_at = Column(DateTime, default=datetime.utcnow)


class StrategyState(Base):
    """Single-row table tracking progress toward monetization goal."""
    __tablename__ = "strategy_state"
    id = Column(Integer, primary_key=True)
    subs = Column(Integer, default=0)
    watch_hours_12mo = Column(Float, default=0.0)
    shorts_views_90d = Column(Integer, default=0)
    active_track = Column(String(20), default="long")  # long | shorts
    last_evaluated_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text, nullable=True)

    # niche discovery phase
    phase = Column(String(20), default="niche_discovery")  # niche_discovery | locked
    discovery_started_at = Column(DateTime, nullable=True)
    discovery_ends_at = Column(DateTime, nullable=True)
    locked_niche = Column(String(100), nullable=True)
    branding_last_applied_at = Column(DateTime, nullable=True)


class Genome(Base):
    """
    A versioned bundle of prompt templates + pacing params. The active
    'control' genome is what production defaults to; 'candidate' genomes
    are mutations currently being A/B tested; 'retired' ones lost.
    """
    __tablename__ = "genomes"
    id = Column(Integer, primary_key=True)
    version = Column(Integer, unique=True, nullable=False)
    status = Column(String(20), default="candidate")  # control | candidate | retired
    parent_version = Column(Integer, nullable=True)

    ideation_system_prompt = Column(Text)
    script_system_prompt = Column(Text)
    seo_system_prompt = Column(Text)
    thumbnail_style_prompt = Column(Text)  # appended to every image prompt

    scene_count_long = Column(Integer, default=10)
    scene_count_shorts = Column(Integer, default=5)
    length_note_long = Column(String(255), default="5-8 minutes")
    length_note_shorts = Column(String(255), default="under 60 seconds")

    mutation_rationale = Column(Text, nullable=True)  # why this variant was proposed
    videos_produced = Column(Integer, default=0)
    avg_ctr = Column(Float, nullable=True)
    avg_retention = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    promoted_at = Column(DateTime, nullable=True)
    retired_at = Column(DateTime, nullable=True)


class CompetitorInsight(Base):
    """LLM-synthesized patterns from top-performing public videos in a topic."""
    __tablename__ = "competitor_insights"
    id = Column(Integer, primary_key=True)
    topic = Column(String(255))
    format = Column(String(20))
    summary = Column(Text)          # what seems to be working (hooks, titles, pacing, thumbnails)
    source_video_ids = Column(Text)  # comma-separated youtube video ids used as evidence
    scraped_at = Column(DateTime, default=datetime.utcnow)


class Rule(Base):
    """Knowledge Base: durable rules learned over time across experiments."""
    __tablename__ = "knowledge"
    id = Column(Integer, primary_key=True)
    rule = Column(Text, nullable=False)
    category = Column(String(50), default="general")  # hook | title | thumbnail | length | topic | voice | pacing
    confidence = Column(Float, default=0.5)  # 0.0 to 1.0
    evidence_count = Column(Integer, default=1)
    metrics_impacted = Column(String(255), default="ctr,retention")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class Experiment(Base):
    """Experiment Engine: explicit single-variable testing tracking per upload."""
    __tablename__ = "experiments"
    id = Column(Integer, primary_key=True)
    video_id = Column(Integer, nullable=True)
    variable = Column(String(100), nullable=False)  # e.g., hook_type, thumbnail_style, title_structure
    old_value = Column(Text, nullable=True)
    new_value = Column(Text, nullable=True)
    hypothesis = Column(Text, nullable=False)
    result = Column(String(30), default="pending")  # pending | confirmed | refuted | inconclusive
    created_at = Column(DateTime, default=datetime.utcnow)
    evaluated_at = Column(DateTime, nullable=True)


class Strategy(Base):
    """Strategy Engine: generated strategy reading from Knowledge Base before production."""
    __tablename__ = "strategies"
    id = Column(Integer, primary_key=True)
    summary = Column(Text, nullable=False)
    reasoning = Column(Text, nullable=True)
    mutation_plan = Column(Text, nullable=True)
    risk_level = Column(String(20), default="moderate")  # low | moderate | high
    created_at = Column(DateTime, default=datetime.utcnow)


class AnalyticsSnapshot(Base):
    """Analytics Collector: rich snapshots of performance over time."""
    __tablename__ = "analytics_snapshots"
    id = Column(Integer, primary_key=True)
    video_id = Column(Integer, nullable=True)
    youtube_id = Column(String(64), nullable=True)
    impressions = Column(Integer, default=0)
    ctr = Column(Float, default=0.0)
    views = Column(Integer, default=0)
    watch_time_hours = Column(Float, default=0.0)
    avg_view_duration_sec = Column(Float, default=0.0)
    retention_pct = Column(Float, default=0.0)
    subscribers_gained = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    fitness_score = Column(Float, default=0.0)
    snapshot_at = Column(DateTime, default=datetime.utcnow)


DEFAULT_IDEATION_PROMPT = (
    "You are a YouTube content strategist for a faceless AI-generated channel. "
    "Generate ONE video idea. Respond ONLY as JSON with keys: "
    "title, topic, format, hook, outline (array of 3-6 beat strings)."
)
DEFAULT_SCRIPT_PROMPT = (
    "You write narration scripts for a faceless AI YouTube video. "
    "Respond ONLY as JSON: {\"scenes\": [{\"narration\": str, \"image_prompt\": str}, ...]}. "
    "narration = spoken text for that scene (natural spoken English, no stage directions). "
    "image_prompt = a vivid, safe-for-work, copyright-free visual description "
    "(no real people, no brand logos, no copyrighted characters) suitable for an "
    "AI image generator."
)
DEFAULT_SEO_PROMPT = (
    "You write YouTube SEO metadata. Respond ONLY as JSON: "
    "{\"title\": str, \"description\": str, \"tags\": [str, ...]}. "
    "Title under 100 chars. Description 3-5 sentences plus a soft CTA to subscribe, "
    "include 3-5 relevant hashtags at the end. 10-15 tags."
)
DEFAULT_THUMBNAIL_STYLE = "vivid colors, high contrast, bold focal subject, clean composition"


def init_db():
    os.makedirs(os.path.dirname(os.getenv("DB_PATH", "./db/agent.db")) or ".", exist_ok=True)
    Base.metadata.create_all(engine)

    session = get_session()
    if not session.query(Genome).first():
        seed = Genome(
            version=1,
            status="control",
            ideation_system_prompt=DEFAULT_IDEATION_PROMPT,
            script_system_prompt=DEFAULT_SCRIPT_PROMPT,
            seo_system_prompt=DEFAULT_SEO_PROMPT,
            thumbnail_style_prompt=DEFAULT_THUMBNAIL_STYLE,
            mutation_rationale="Initial seed genome.",
            promoted_at=datetime.utcnow(),
        )
        session.add(seed)
        session.commit()

    if not session.query(Rule).first():
        seed_rules = [
            Rule(rule="Hooks opening with high-stakes mysteries or bold contradictions perform better than generic introductions.", category="hook", confidence=0.7, evidence_count=2, metrics_impacted="retention"),
            Rule(rule="Titles formatted as punchy formulas (e.g. 'Why X Solved Y' or 'The X That No One Explained') drive higher click-through rates.", category="title", confidence=0.8, evidence_count=3, metrics_impacted="ctr"),
            Rule(rule="Bright, illuminated, high-contrast graphic novel illustrations out-perform dark pitch-black shadowy thumbnails.", category="thumbnail", confidence=0.85, evidence_count=4, metrics_impacted="ctr"),
            Rule(rule="Pacing scenes to roughly 15 words (~7 seconds each) maintains steady viewer retention.", category="pacing", confidence=0.75, evidence_count=2, metrics_impacted="retention"),
        ]
        session.add_all(seed_rules)
        session.commit()

    session.close()


def get_session():
    return SessionLocal()

