# backend/openrouter.py
import json
from pathlib import Path
import httpx
from fastapi import HTTPException

def load_api_key() -> str:
    current_dir = Path(__file__).resolve().parent
    config_path = current_dir / "config.json"
    if not config_path.exists():
        raise RuntimeError(f"config.json not found at {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)
    api_key = cfg.get("OPENROUTER_API_KEY")
    if not api_key or api_key.startswith("<"):
        raise RuntimeError("OPENROUTER_API_KEY missing or looks invalid in config.json")
    return api_key

OPENROUTER_API_KEY = load_api_key()
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"


async def openrouter_complete(messages, model: str = "openai/gpt-4.1-mini", max_tokens: int = 512, temperature: float = 0.1) -> str:
    """
    Send messages to OpenRouter and return assistant text.
    Defaults use a smaller model and token limit to avoid credit/token issues.
    Raises HTTPException on upstream errors with helpful details.
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",  # optional
        "X-Title": "TraderGPT Pro",                # optional
    }

    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    async with httpx.AsyncClient(timeout=120) as client:
        try:
            resp = await client.post(BASE_URL, json=payload, headers=headers)
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            status = e.response.status_code
            body = e.response.text
            # Log details server-side for debugging (do not log the API key)
            print("OpenRouter error status:", status)
            print("OpenRouter error body:", body)
            # Return helpful error to client
            raise HTTPException(status_code=502, detail=f"OpenRouter error {status}: {body}")
        except Exception as e:
            print("OpenRouter unexpected error:", repr(e))
            raise HTTPException(status_code=502, detail=f"OpenRouter unexpected error: {repr(e)}")

        data = resp.json()
        try:
            return data["choices"][0]["message"]["content"]
        except Exception:
            raise HTTPException(status_code=502, detail=f"OpenRouter response format unexpected: {data}")
