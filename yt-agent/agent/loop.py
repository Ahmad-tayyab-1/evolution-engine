import os
import time
import random
import tempfile
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

from agent.db import init_db, get_session, Video, CommentQueue, Genome, StrategyState, Strategy, Experiment, Rule  # noqa: E402
from agent import ideation, scriptgen, imagegen, tts, assemble, strategy, evolve, niche_discovery, branding, candidate, experiment  # noqa: E402
from agent import youtube_client as yt  # noqa: E402
from agent.llm import chat  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("yt-agent")

INTERVAL_MIN = int(os.getenv("LOOP_INTERVAL_MINUTES", 30))
UPLOAD_CAP = int(os.getenv("UPLOADS_PER_DAY_CAP", 6))
AUTO_REPLY = os.getenv("COMMENT_AUTO_REPLY", "false").lower() == "true"
EVOLVE_EVERY_N_CYCLES = int(os.getenv("EVOLVE_EVERY_N_CYCLES", 12))  # ~every 6h at 30min interval
CANDIDATE_TRAFFIC_SHARE = float(os.getenv("CANDIDATE_TRAFFIC_SHARE", 0.3))  # 30% of videos try the candidate


def _uploads_today(session) -> int:
    since = datetime.utcnow() - timedelta(hours=24)
    return session.query(Video).filter(Video.status == "uploaded", Video.published_at >= since).count()


def _pick_genome(session) -> Genome:
    """A/B selection: mostly control, some traffic to the active candidate (if any)."""
    control = session.query(Genome).filter_by(status="control").first()
    candidate_gen = session.query(Genome).filter_by(status="candidate").first()
    if candidate_gen and random.random() < CANDIDATE_TRAFFIC_SHARE:
        return candidate_gen
    return control


def produce_and_publish_one_video():
    session = get_session()
    if _uploads_today(session) >= UPLOAD_CAP:
        log.info("Daily upload cap reached, skipping production this cycle.")
        session.close()
        return

    genome = _pick_genome(session)
    if not genome:
        log.error("No genome found - run init_db() first.")
        session.close()
        return

    # Module 5: Strategy Engine
    state, strat = strategy.run_full_cycle()

    # Base topic generation
    base_idea = ideation.generate_video_idea(genome)
    
    # Module 4: Experiment Engine (single-variable test hypothesis setup)
    dummy_vid = Video(title=base_idea["title"], topic=base_idea["topic"], format=base_idea["format"], status="planned", genome_version=genome.version, niche=base_idea.get("niche"), strategy_id=strat.id if strat else None)
    session.add(dummy_vid)
    session.commit()
    vid_id = dummy_vid.id

    exp_id, exp_injection = experiment.formulate_experiment(genome, vid_id, base_idea["format"])
    dummy_vid.experiment_id = exp_id

    # Module 6 & 7: Candidate Generator & Quality Evaluator
    idea = candidate.generate_and_evaluate_candidates(genome, base_idea["topic"], base_idea["format"], experiment_injection=exp_injection)
    dummy_vid.title = idea["title"]
    dummy_vid.topic = idea["topic"]
    session.commit()
    video = dummy_vid
    log.info(f"Idea Selected by Quality Evaluator: {idea['title']} ({idea['format']}) [exp={exp_id}] [genome v{genome.version}]")

    with tempfile.TemporaryDirectory(prefix="ytagent_") as work_dir:
        try:
            script = scriptgen.generate_script(idea, genome)
            video.status = "scripted"
            session.commit()

            vertical = idea["format"] == "shorts"
            image_paths = imagegen.generate_scene_images(
                script["scenes"], work_dir, vertical=vertical,
                style_prompt=genome.thumbnail_style_prompt,
            )
            audio_paths = tts.synthesize_scenes(script["scenes"], work_dir)
            video.status = "assets_ready"
            session.commit()

            out_video_path = os.path.join(work_dir, "final.mp4")
            assemble.assemble_video(image_paths, audio_paths, work_dir, out_video_path, vertical=vertical)

            thumb_path = os.path.join(work_dir, "thumb.jpg")
            assemble.make_thumbnail(image_paths[0], thumb_path)
            video.status = "assembled"
            session.commit()

            seo = scriptgen.generate_seo_metadata(idea, script, genome)
            youtube_id = yt.upload_video(
                video_path=out_video_path,
                title=seo["title"],
                description=seo["description"],
                tags=seo["tags"],
                thumbnail_path=thumb_path,
            )

            video.youtube_id = youtube_id
            video.status = "uploaded"
            video.published_at = datetime.utcnow()
            session.commit()
            log.info(f"Uploaded: {seo['title']} -> https://youtu.be/{youtube_id}")

        except Exception as e:
            video.status = "failed"
            video.error = str(e)
            session.commit()
            log.exception("Video production failed")

    session.close()


def poll_and_queue_comments():
    session = get_session()
    comments = yt.fetch_new_comments()
    for c in comments:
        exists = session.query(CommentQueue).filter_by(youtube_comment_id=c["comment_id"]).first()
        if exists:
            continue
        draft = chat(
            system=(
                "You reply to YouTube comments as a friendly channel persona. "
                "Keep replies under 2 sentences, warm, no spam links, no over-promising."
            ),
            user=f"Comment: {c['text']}",
            temperature=0.6,
        )
        row = CommentQueue(
            youtube_comment_id=c["comment_id"], video_youtube_id=c["video_id"],
            author=c["author"], text=c["text"], draft_reply=draft,
            status="approved" if AUTO_REPLY else "pending",
        )
        session.add(row)
        if AUTO_REPLY:
            yt.post_reply(c["comment_id"], draft)
            row.status = "posted"
    session.commit()
    session.close()


def run_forever():
    init_db()
    log.info("YT agent starting. Loop interval: %s min", INTERVAL_MIN)

    # kick off niche discovery on first-ever run
    session = get_session()
    state = session.query(StrategyState).first()
    needs_start = not state or not state.discovery_ends_at
    session.close()
    if needs_start:
        days = int(os.getenv("NICHE_DISCOVERY_DAYS", 5))
        log.info(f"Starting niche discovery phase ({days} days)...")
        niche_discovery.start_discovery(days=days)

    cycle_count = 0
    while True:
        try:
            strategy.run_full_cycle()
            niche_discovery.update_niche_performance()
            niche_discovery.maybe_conclude_discovery()
            branding.apply_initial_branding()  # no-op unless niche just locked and not yet applied
            branding.maybe_refresh_branding()  # no-op unless due
            produce_and_publish_one_video()
            poll_and_queue_comments()

            cycle_count += 1
            if cycle_count % EVOLVE_EVERY_N_CYCLES == 0:
                log.info("Running evolution cycle (competitor scan + genome evaluation)...")
                evolve.run_evolution_cycle()
        except Exception:
            log.exception("Cycle error, continuing loop")
        time.sleep(INTERVAL_MIN * 60)


if __name__ == "__main__":
    run_forever()
