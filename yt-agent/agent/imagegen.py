import os
import random
import logging
import urllib.parse
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from PIL import Image, ImageDraw, ImageFont

log = logging.getLogger(__name__)

BASE_URL = os.getenv("POLLINATIONS_BASE_URL", "https://image.pollinations.ai/prompt")

# Rotating residential proxies to avoid 403/rate limits
PROXY_USER = "fltfbbcd"
PROXY_PASS = "nrfoc9awe3xl"
PROXY_LIST = [
    "31.59.20.176:6754",
    "31.56.127.193:7684",
    "45.38.107.97:6014",
    "198.105.121.200:6462",
    "64.137.96.74:6641",
    "198.23.243.226:6361",
    "38.154.185.97:6370",
    "84.247.60.125:6095",
    "142.111.67.146:5611",
    "191.96.254.138:6185",
]


def _get_proxy():
    """Pick a random proxy from the pool and return a requests-compatible dict."""
    host_port = random.choice(PROXY_LIST)
    proxy_url = f"http://{PROXY_USER}:{PROXY_PASS}@{host_port}"
    return {"http": proxy_url, "https": proxy_url}


def _create_fallback_image(out_path: str, width: int, height: int, prompt: str = ""):
    """Generate a gradient placeholder image when the API is unavailable."""
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)
    for y in range(height):
        r = int(15 + (y / height) * 25)
        g = int(10 + (y / height) * 20)
        b = int(30 + (y / height) * 50)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    try:
        font = ImageFont.load_default()
        short = prompt[:80] + "..." if len(prompt) > 80 else prompt
        draw.text((width // 2 - 200, height // 2), short, fill=(80, 80, 120), font=font)
    except Exception:
        pass
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path)
    return out_path


@retry(
    stop=stop_after_attempt(6),
    wait=wait_exponential(multiplier=3, min=3, max=30),
    retry=retry_if_exception_type((
        requests.exceptions.HTTPError,
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout,
        requests.exceptions.ProxyError,
    )),
)
def generate_image(prompt: str, out_path: str, width: int = 1024, height: int = 1024, seed: int | None = None):
    encoded = urllib.parse.quote(prompt)
    url = f"{BASE_URL}/{encoded}"
    params = {"width": width, "height": height, "nologo": "true"}
    if seed is not None:
        params["seed"] = seed

    proxy = _get_proxy()
    log.debug(f"Image request via proxy {list(proxy.values())[0].split('@')[1]}")

    resp = requests.get(url, params=params, proxies=proxy, timeout=90)
    resp.raise_for_status()

    content_type = resp.headers.get("content-type", "")
    if "image" not in content_type and len(resp.content) < 1000:
        raise requests.exceptions.HTTPError(f"Expected image, got {content_type}")

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(resp.content)
    return out_path


def generate_scene_images(scenes: list, work_dir: str, vertical: bool = False, style_prompt: str = "") -> list:
    """Generates one image per scene, returns list of file paths in order.
    style_prompt comes from the active genome and evolves over time.
    Falls back to placeholder images if the API is unavailable."""
    w, h = (1080, 1920) if vertical else (1920, 1080)
    paths = []
    for i, scene in enumerate(scenes):
        prompt = f"{scene['image_prompt']}, {style_prompt}" if style_prompt else scene["image_prompt"]
        out = os.path.join(work_dir, "images", f"scene_{i:02d}.png")
        try:
            generate_image(prompt, out, width=w, height=h, seed=i)
            log.info(f"Scene {i} image generated OK")
        except Exception as e:
            log.warning(f"Image generation failed for scene {i}, using fallback: {e}")
            _create_fallback_image(out, w, h, prompt)
        paths.append(out)
    return paths
