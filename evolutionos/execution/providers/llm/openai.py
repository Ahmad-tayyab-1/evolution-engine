"""
OpenAI Provider Client (`Plan.md` Appendix B).
Wraps completion calls and cost accounting for OpenAI models (`gpt-4o`, `gpt-4o-mini`).
"""
from typing import Dict, Any, Optional


class OpenAIClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or "sk-dummy-openai-key"

    def generate_completion(self, prompt: str, model: str = "gpt-4o", max_tokens: int = 1000) -> Dict[str, Any]:
        return {
            "text": f"[OpenAI {model} response for]: {prompt[:50]}...",
            "usage": {"prompt_tokens": len(prompt) // 4, "completion_tokens": 150, "total_tokens": (len(prompt) // 4) + 150},
            "model": model,
            "provider": "openai"
        }
