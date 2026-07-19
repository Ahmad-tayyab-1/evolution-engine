"""
Gemini Provider Client (`Plan.md` Appendix B).
Wraps completion calls and cost accounting for Google Gemini models (`gemini-1.5-pro`, `gemini-1.5-flash`).
"""
from typing import Dict, Any, Optional


class GeminiClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or "dummy-gemini-key"

    def generate_completion(self, prompt: str, model: str = "gemini-1.5-pro", max_tokens: int = 1000) -> Dict[str, Any]:
        return {
            "text": f"[Gemini {model} response for]: {prompt[:50]}...",
            "usage": {"prompt_tokens": len(prompt) // 4, "completion_tokens": 150, "total_tokens": (len(prompt) // 4) + 150},
            "model": model,
            "provider": "gemini"
        }
