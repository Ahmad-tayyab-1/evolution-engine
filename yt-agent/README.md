# yt-agent

Autonomous faceless YouTube channel agent. Generates ideas → script → images
(pollinations.ai) → voice (Deepgram) → video (ffmpeg) → uploads → monitors
comments → tracks progress toward YouTube Partner Program monetization
thresholds and re-weights future content accordingly.

## 1. Setup

```bash
cd yt-agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# ffmpeg must be on PATH
sudo apt install -y ffmpeg

cp .env.example .env
# edit .env: GROQ_API_KEY, DEEPGRAM_API_KEY, POLLINATIONS_API_KEY, YT_CLIENT_SECRET_FILE path
```

## 2. YouTube OAuth (one-time)

1. In Google Cloud Console: enable **YouTube Data API v3** and
   **YouTube Analytics API**, create an OAuth Client ID (Desktop app type),
   download as `secrets/client_secret.json`.
2. Run:
   ```bash
   python -m agent.auth_setup
   ```
   This opens a browser, you authorize against your channel once. Saves
   `secrets/token.json` — the loop reuses/refreshes this unattended after.

## 3. Test one cycle manually

```bash
python -c "from agent.loop import produce_and_publish_one_video, init_db; init_db(); produce_and_publish_one_video()"
```

Check `db/agent.db` (or your configured backend) for the `videos` row and
its `status`/`error` fields if something fails partway.

## 4. Review comment replies (if COMMENT_AUTO_REPLY=false)

```bash
python -m agent.review_comments
```

## 5. Run as a persistent service

```bash
sudo cp yt-agent.service /etc/systemd/system/yt-agent@$(whoami).service
sudo systemctl daemon-reload
sudo systemctl enable --now yt-agent@$(whoami)
journalctl -u yt-agent@$(whoami) -f
```

## Channel branding (description + keywords only)

Once niche discovery locks in, the agent auto-writes and applies the
**channel description and keywords** (`agent/branding.py`), and refreshes
them every `BRANDING_REFRESH_DAYS` (default 14) using whichever topics are
performing best by then.

**Profile picture, banner, and channel name are never touched** — those
stay fully manual, by design. Branding metadata is low-risk to automate
(easy to see, easy to revert) and benefits from the same iterative SEO
approach as video metadata; visual identity is a one-time decision better
made by a person.

## Niche discovery phase

You don't pick the channel's niche upfront — the agent tests several and
picks based on real performance:

1. **Candidates** (`agent/niches.py`): 5 distinct, advertiser-friendly
   candidate niches (science/space, history mysteries, true crime, psychology,
   tech explained), each with a pool of seed topics. Edit this list before
   first run if any don't fit what you want the channel to be — the agent
   won't invent niches outside this list. Kept deliberately small so each
   niche gets a real sample within the discovery window, and money/finance
   was left out since it's more advertiser-sensitive for a brand-new channel.
2. **Pre-scan** (day 0): quick public-search check per niche — view
   velocity of recent top videos as a rough demand signal. This only
   biases which niches get sampled *first*, it doesn't decide the winner.
3. **Exploration** (`NICHE_DISCOVERY_DAYS`, default 5): production spreads
   across all 5 candidate niches, weighted toward ones showing early promise
   (blend of the pre-scan signal and real CTR/retention as videos get
   metrics). At the default `UPLOADS_PER_DAY_CAP=6`, 5 days gives roughly
   6 videos per niche — enough to not lock in on a single lucky/unlucky
   upload.
4. **Lock-in**: once the window closes AND every niche has at least
   `NICHE_MIN_VIDEOS` (default 4) measured videos, the niche with the best
   combined CTR+retention is locked in. If data's still thin when the
   window closes, it grants a 12h grace period rather than locking on
   noise. From then on, all topics come from the winning niche only — the
   evolve/strategy engines keep optimizing inside it as before.

Check progress any time:
```bash
python -m agent.niche_status
```

## Self-evolution system

The agent doesn't just re-weight topics — it evolves the actual prompt
templates and pacing over time:

- **Genome** (`agent/db.py::Genome`): a versioned bundle of the ideation/
  script/SEO system prompts, thumbnail style, and scene-count/length pacing.
  One genome is always `control` (production default).
- **Competitor scan** (`agent/competitor_scan.py`): every evolution cycle,
  pulls public top-velocity videos in your active topics via YouTube search
  (title/tag/duration patterns only — no private competitor data) and has
  the LLM synthesize what seems to be working.
- **Mutation** (`agent/evolve.py::propose_mutation`): given your own
  top-performing videos under the current genome + competitor patterns, the
  LLM proposes ONE testable change (e.g. punchier hooks, different scene
  count, new title structure) as a `candidate` genome.
- **A/B rollout**: `CANDIDATE_TRAFFIC_SHARE` (default 30%) of new videos use
  the candidate genome instead of control; the rest stay on control as the
  baseline.
- **Promotion/retirement**: once a candidate has `EVOLVE_MIN_SAMPLE`
  (default 4) uploaded videos with metrics, its avg CTR+retention is
  compared to control's. Beats it by `EVOLVE_IMPROVEMENT_MARGIN` (default
  10%) → promoted to `control`, old control retired. Loses by that margin →
  retired. Otherwise it keeps running until it has enough data.
- Only **one candidate runs at a time** to keep comparisons clean.

Check what it's tried and why:
```bash
python -m agent.genome_status
```

## Notes / things to watch

- **Quota**: `videos.insert` costs 1,600 units. Default daily quota is
  10,000 units → ~6 uploads/day. Your 3-stage-verified channel may have a
  higher quota already; adjust `UPLOADS_PER_DAY_CAP` in `.env` accordingly.
  If you want the ~100/day headroom, request a quota increase in Cloud
  Console (Audit and Compliance > YouTube API Services).
- **Monetization tracking**: `strategy_state` table tracks subs, 12-month
  watch hours, and 90-day Shorts views against YPP thresholds
  (1,000 subs + 4,000 watch hrs, OR 1,000 subs + 10M Shorts views/90d),
  and biases the `active_track` (long vs shorts) toward whichever is closer.
- **Comment auto-reply** defaults to a review queue (`COMMENT_AUTO_REPLY=false`)
  — flip to `true` in `.env` once you trust reply quality.
- **Content policy**: keep topic variety high — YouTube's repetitive/
  mass-produced content policy affects monetization eligibility for
  AI-generated channels.
