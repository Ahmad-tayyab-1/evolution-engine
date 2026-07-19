import os
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
VOICE_MODEL = os.getenv("DEEPGRAM_VOICE_MODEL", "aura-asteria-en")
TTS_URL = "https://api.deepgram.com/v1/speak"


DEEPGRAM_VOICE_POOL = [
    "aura-asteria-en",  # US English Female (conversational, warm)
    "aura-luna-en",     # US English Female (soft, engaging)
    "aura-stella-en",   # US English Female (bright, upbeat)
    "aura-athena-en",   # UK English Female (calm, authoritative)
    "aura-hera-en",     # US English Female (smooth, mature)
    "aura-orion-en",    # US English Male (deep, narrator)
    "aura-arcas-en",    # US English Male (energetic, friendly)
    "aura-perseus-en",  # US English Male (rich, authoritative)
    "aura-angus-en",    # Irish English Male (distinctive, engaging)
    "aura-orpheus-en",  # US English Male (conversational, clear)
    "aura-helios-en",   # UK English Male (polished, clear)
    "aura-zeus-en",     # US English Male (commanding, deep)
    "aura-zenobia-en",  # US English Female (expressive, dynamic)
    "aura-sylvia-en",   # US English Female (professional, clear)
    "aura-harmonia-en", # US English Female (gentle, clear)
    "aura-theia-en",    # Australian English Female (friendly, distinct)
    "aura-dionysus-en", # US English Male (warm, storytelling)
    "aura-hyperion-en", # US English Male (strong, upbeat)
    "aura-iris-en",     # US English Female (clear, bright)
    "aura-phoebe-en"    # US English Female (youthful, energetic)
]


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2, min=2, max=15))
def synthesize(text: str, out_path: str, voice_model: str = None) -> str:
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "application/json",
    }
    model_to_use = voice_model or VOICE_MODEL
    params = {"model": model_to_use, "encoding": "linear16", "sample_rate": 24000}
    resp = requests.post(TTS_URL, headers=headers, params=params, json={"text": text}, timeout=60)
    resp.raise_for_status()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(resp.content)
    return out_path


def synthesize_scenes(scenes: list, work_dir: str, voice_model: str = None) -> list:
    """One WAV per scene, returns list of file paths in order."""
    paths = []
    for i, scene in enumerate(scenes):
        out = os.path.join(work_dir, "audio", f"scene_{i:02d}.wav")
        synthesize(scene["narration"], out, voice_model=voice_model)
        paths.append(out)
    return paths
