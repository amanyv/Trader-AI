import json
import httpx
from pathlib import Path

BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

def load_key():
    path = Path(__file__).parent / "config.json"
    return json.load(open(path))["OPENROUTER_API_KEY"]

API_KEY = load_key()

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

async def llm_complete(messages, max_tokens=500):
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(
            BASE_URL,
            headers=HEADERS,
            json={
                "model": "openai/gpt-4.1-mini",
                "messages": messages,
                "temperature": 0.1,
                "max_tokens": max_tokens
            }
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
