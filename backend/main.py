# backend/main.py
import json
from typing import Any, Dict, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from openrouter import openrouter_complete

# ------------------------
# Pydantic models
# ------------------------
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

class AnalyzeRequest(BaseModel):
    symbol: str
    horizon: str

class AnalyzeResponse(BaseModel):
    symbol: str
    horizon: str
    bias: str
    summary: str
    reasons: List[str]
    risks: List[str]
    trade_idea: Dict[str, str]
    sources: List[Dict[str, str]]

# ------------------------
# App setup
# ------------------------
app = FastAPI(title="TraderGPT Pro Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # OK for local dev; lock down for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root() -> Dict[str, str]:
    return {"status": "TraderGPT Pro backend running"}

# ------------------------
# /api/chat
# ------------------------
@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest) -> ChatResponse:
    messages = [
        {"role": "system", "content": "You are an AI trading research assistant. Answer concisely and clearly."},
        {"role": "user", "content": req.message},
    ]
    # Smaller token usage for chat
    reply = await openrouter_complete(messages, model="openai/gpt-4.1-mini", max_tokens=256, temperature=0.2)
    return ChatResponse(reply=reply)

# ------------------------
# /api/analyze-symbol
# ------------------------
@app.post("/api/analyze-symbol", response_model=AnalyzeResponse)
async def analyze_symbol(req: AnalyzeRequest) -> AnalyzeResponse:
    """
    Ask LLM to return a compact JSON analysis. Defaults chosen to reduce token usage.
    """

    system_prompt = """
You are TraderGPT Pro, an AI trading research assistant.
Respond ONLY with a compact JSON object that matches the schema exactly.
Keep responses concise and under ~500 tokens.
Schema:
{
  "symbol":"RELIANCE",
  "horizon":"2-3 weeks",
  "bias":"moderately bullish",
  "summary":"string",
  "reasons":["string","string"],
  "risks":["string","string"],
  "trade_idea":{
    "direction":"long or short",
    "entry_zone":"string",
    "stop_loss":"string",
    "target":"string",
    "notes":"string"
  },
  "sources":[{"title":"string","snippet":"string"}]
}
"""

    user_prompt = f"Analyze {req.symbol} for horizon {req.horizon}. No extra text — JSON only. Keep it short."

    messages = [
        {"role": "system", "content": system_prompt.strip()},
        {"role": "user", "content": user_prompt.strip()},
    ]

    # Use smaller token limit to avoid 402 credit errors
    raw_reply = await openrouter_complete(messages, model="openai/gpt-4.1-mini", max_tokens=512, temperature=0.1)

    # Try to parse JSON; be defensive if model wraps with text
    try:
        data: Any = json.loads(raw_reply)
    except json.JSONDecodeError:
        start = raw_reply.find("{")
        end = raw_reply.rfind("}")
        if start != -1 and end != -1 and end > start:
            json_str = raw_reply[start:end+1]
            data = json.loads(json_str)
        else:
            data = {
                "symbol": req.symbol,
                "horizon": req.horizon,
                "bias": "neutral",
                "summary": "Model returned unparsable output.",
                "reasons": ["Parsing error."],
                "risks": ["Parsing error."],
                "trade_idea": {
                    "direction": "long",
                    "entry_zone": "N/A",
                    "stop_loss": "N/A",
                    "target": "N/A",
                    "notes": "Check backend logs."
                },
                "sources": []
            }

    # Ensure required fields and defaults
    data.setdefault("symbol", req.symbol)
    data.setdefault("horizon", req.horizon)
    data.setdefault("bias", "neutral")
    data.setdefault("summary", "")
    data.setdefault("reasons", [])
    data.setdefault("risks", [])
    data.setdefault("trade_idea", {})
    data.setdefault("sources", [])

    ti = data["trade_idea"]
    ti.setdefault("direction", "long")
    ti.setdefault("entry_zone", "N/A")
    ti.setdefault("stop_loss", "N/A")
    ti.setdefault("target", "N/A")
    ti.setdefault("notes", "")

    return AnalyzeResponse(
        symbol=data["symbol"],
        horizon=data["horizon"],
        bias=data["bias"],
        summary=data["summary"],
        reasons=data["reasons"],
        risks=data["risks"],
        trade_idea=ti,
        sources=data["sources"]
    )
