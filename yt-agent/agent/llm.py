import os
import json
from groq import Groq
from tenacity import retry, stop_after_attempt, wait_exponential

_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=2, min=2, max=20))
def chat(system: str, user: str, json_mode: bool = False, temperature: float = 0.8) -> str:
    kwargs = {}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    resp = _client.chat.completions.create(
        model=MODEL,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        **kwargs,
    )
    return resp.choices[0].message.content


def chat_json(system: str, user: str, temperature: float = 0.7) -> dict:
    raw = chat(system, user, json_mode=True, temperature=temperature)
    return json.loads(raw)
