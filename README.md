# Evolution Engine & Autonomous YouTube Agent

An autonomous, self-improving video production and multi-agent channel orchestration framework (`EvolutionOS` + `yt-agent`). This platform autonomously generates ideas, scripts, images, voiceovers, and videos, publishes them directly to YouTube, tracks real-time monetization metrics, and self-evolves content strategies based on audience performance.

---

## 🏗️ System Architecture

The project consists of two primary subsystems:

### 1. `evolutionos/` — The Core Multi-Agent & Governance OS
An enterprise-grade, event-driven architecture that governs AI decision-making, content policies, learning loops, and simulation workflows.
- **`core/`**: Domain models (`ontology.py`), reasoning engines (`belief_engine.py`, `calibration_engine.py`, `decision_engine.py`, `strategy_engine.py`), and saga workflows (`evolution_cycle_saga.py`).
- **`execution/`**: Pipeline stages for autonomous media production (`research`, `story`, `script`, `visual_planning`, `composition`, `narration`, `publishing`).
- **`governance/`**: Safety constraints (`kill_switch.py`, `policy_engine.py`, `content_policy.py`, `forbidden_registry.py`) ensuring brand-safe, monetizable output.
- **`dashboard/`**: FastAPI backend providing live projections, metrics, and remote control over the agent lifecycle.

### 2. `yt-agent/` — The Autonomous YouTube Channel Agent
The operational daemon that runs continuously on production servers (`yt-agent.service`).
- **Content Pipeline**:
  - **Ideation & Strategy**: Scans competitor trends (`competitor_scan.py`) and generates high-CTR concepts (`ideation.py`, `niche_discovery.py`).
  - **Scripting**: Uses Groq/OpenAI to generate structured, retention-optimized scripts (`scriptgen.py`).
  - **Visuals**: Integrates with **`https://gen.pollinations.ai/image`** using Bring Your Own Pollen (BYOP) API keys (`sk_...`) for ultra-fast, high-volume cinematic image generation (`imagegen.py`).
  - **Narration**: Uses **Deepgram** TTS (`tts.py`) for human-sounding, studio-quality narration.
  - **Assembly**: Renders scenes into 1080p/4K MP4 videos using `ffmpeg` (`assemble.py`).
  - **Publishing & Analytics**: Uploads directly via YouTube Data API v3 (`youtube_client.py`) and monitors watch time/monetization thresholds (`fitness.py`, `evolve.py`).
- **Dashboard (`yt-agent/dashboard/`)**: Web UI (`index.html`, `login.html`) to view live logs, metrics, video history, and agent state.

---

## 🚀 Quick Start & Installation

### 1. Prerequisites
- **Python 3.10+** (Tested on Python 3.12)
- **FFmpeg** (`sudo apt install -y ffmpeg` or `winget install Gyan.FFmpeg`)
- **API Keys**:
  - `GROQ_API_KEY` (Text generation & scriptwriting)
  - `DEEPGRAM_API_KEY` (High-quality voice narration)
  - `POLLINATIONS_API_KEY` (Bring Your Own Pollen secret key `sk_...` from [enter.pollinations.ai](https://enter.pollinations.ai))
  - `YT_CLIENT_SECRET_FILE` (Google Cloud OAuth 2.0 Client Secret JSON)

### 2. Environment Setup

Clone the repository and initialize the Python virtual environment:

```bash
git clone https://github.com/Ahmad-tayyab-1/evolution-engine.git
cd evolution-engine

# Setup yt-agent environment
cd yt-agent
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configuration (.env)

Copy the example configuration and populate your keys:

```bash
cp .env.example .env
```

Key environment variables inside `yt-agent/.env`:
```ini
# LLM & Voice
GROQ_API_KEY="gsk_your_groq_key_here"
GROQ_MODEL="openai/gpt-oss-120b"
DEEPGRAM_API_KEY="your_deepgram_key_here"
DEEPGRAM_VOICE_MODEL="aura-asteria-en"

# Image Generation (Pollinations BYOP)
POLLINATIONS_BASE_URL="https://gen.pollinations.ai/image"
POLLINATIONS_API_KEY="sk_your_secret_key_here"

# YouTube OAuth & Channel Config
YT_CLIENT_SECRET_FILE="secrets/client_secret.json"
YT_TOKEN_FILE="secrets/token.json"
YT_CHANNEL_NAME="Your Channel Name"

# Cadence & Limits
LOOP_INTERVAL_MINUTES=30
UPLOADS_PER_DAY_CAP=6
```

---

## 🔑 YouTube OAuth Setup (One-Time)

Before starting autonomous production, authorize the agent against your YouTube channel:

1. In Google Cloud Console, enable **YouTube Data API v3** and **YouTube Analytics API**.
2. Create an OAuth 2.0 Client ID (Desktop application) and download the file to `yt-agent/secrets/client_secret.json`.
3. Run the interactive authorization script:
   ```bash
   python -m agent.auth_setup
   ```
4. A browser prompt will open. Sign in and grant access. The script saves your refresh token to `secrets/token.json` for unattended, headless operation.

---

## ⚡ Running & Testing

### Test a Single Production Cycle Manually
To execute one complete cycle (Ideation → Script → Images → TTS → Video Assembly → Upload):
```bash
cd yt-agent
python -c "from agent.loop import produce_and_publish_one_video, init_db; init_db(); produce_and_publish_one_video()"
```

### Run as a Persistent Systemd Service (Linux Server)
```bash
sudo cp yt-agent.service /etc/systemd/system/yt-agent.service
sudo systemctl daemon-reload
sudo systemctl enable --now yt-agent
sudo journalctl -u yt-agent -f
```

---

## 📊 Dashboard Management

The web dashboard allows real-time monitoring of channel growth, agent logs, and candidate genomes.

To run the standalone dashboard locally:
```bash
cd yt-agent
python -m dashboard.app
```
Then open `http://localhost:8000/` in your browser.

When deployed behind Nginx on production (`yt-dashboard.conf`), ensure the server user (`www-data`) has read permissions for systemd journals:
```bash
sudo usermod -aG systemd-journal,adm www-data
sudo systemctl restart yt-dashboard
```

---

## 🧬 Self-Evolution & Niche Discovery

- **Niche Discovery Phase**: During the first `NICHE_DISCOVERY_DAYS` (default 5 days), the agent produces content across 5 candidate niches (Science, History, True Crime, Psychology, Tech). Once minimum video quotas are met (`NICHE_MIN_VIDEOS`), the engine automatically locks into the niche with the highest combined CTR and retention score.
- **Genome Evolution**: Every `EVOLVE_EVERY_N_CYCLES` (default 12 cycles / 6 hours), the engine evaluates candidate genomes (pacing, visual density, hook structures) against control groups. High-performing variations are promoted to permanent strategy defaults.

---

## 📄 License
MIT License.
