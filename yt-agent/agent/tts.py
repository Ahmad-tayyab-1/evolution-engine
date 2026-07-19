import os
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
VOICE_MODEL = os.getenv("DEEPGRAM_VOICE_MODEL", "aura-asteria-en")
TTS_URL = "https://api.deepgram.com/v1/speak"


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2, min=2, max=15))
def synthesize(text: str, out_path: str) -> str:
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "application/json",
    }
    params = {"model": VOICE_MODEL, "encoding": "linear16", "sample_rate": 24000}
    resp = requests.post(TTS_URL, headers=headers, params=params, json={"text": text}, timeout=60)
    resp.raise_for_status()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(resp.content)
    return out_path


def synthesize_scenes(scenes: list, work_dir: str) -> list:
    """One WAV per scene, returns list of file paths in order."""
    paths = []
    for i, scene in enumerate(scenes):
        out = os.path.join(work_dir, "audio", f"scene_{i:02d}.wav")
        synthesize(scene["narration"], out)
        paths.append(out)
    return paths
