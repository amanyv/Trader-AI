import json
from pathlib import Path
import httpx

BASE_CHAT = "https://openrouter.ai/api/v1/chat/completions"
BASE_EMBED = "https://openrouter.ai/api/v1/embeddings"

def load_key():
    path = Path(__file__).parent / "config.json"
    return json.load(open(path))["OPENROUTER_API_KEY"]

API_KEY = load_key()

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

async def llm_complete(messages, max_tokens=600):
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(
            BASE_CHAT,
            headers=HEADERS,
            json={
                "model": "openai/gpt-4.1-mini",
                "messages": messages,
                "max_tokens": max_tokens,
                "temperature": 0.1
            }
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]

async def embed_text(text: str) -> list[float]:
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(
            BASE_EMBED,
            headers=HEADERS,
            json={
                "model": "text-embedding-3-small",
                "input": text
            }
        )
        r.raise_for_status()
        return r.json()["data"][0]["embedding"]
