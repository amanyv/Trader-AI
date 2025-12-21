import json
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
from openrouter import llm_complete
from market_data import get_price_series

app = FastAPI()

# ---- Serve static assets correctly ----
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_index():
    return FileResponse("static/index.html")

# ---- Models ----
class AnalyzeRequest(BaseModel):
    symbol: str
    horizon: str

# ---- APIs ----
@app.post("/api/analyze-symbol")
async def analyze(req: AnalyzeRequest):
    system_prompt = f"""
You are TraderGPT Pro.
Return ONLY valid JSON.

IMPORTANT RULES:
- Always provide Direction, Entry, Stop, Target
- If unsure, still provide reasonable placeholder levels
- Do NOT leave fields empty

Schema:
{{
  "symbol":"{req.symbol}",
  "horizon":"{req.horizon}",
  "bias":"bullish|neutral|bearish",
  "summary":"string",
  "reasons":["string"],
  "risks":["string"],
  "trade_idea": {{
    "direction":"long|short",
    "entry_zone":"string (example: 2500 or 2500-2520)",
    "stop_loss":"string (example: 2440)",
    "target":"string (example: 2620)"
  }}
}}
"""

    raw = await llm_complete([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Analyze {req.symbol} for {req.horizon} trade."}
    ])

    try:
        data = json.loads(raw)
    except Exception:
        data = {}

    # ---------- HARD GUARANTEES ----------
    trade = data.get("trade_idea", {})

    trade.setdefault("direction", "long")
    trade.setdefault("entry_zone", "Market price ± 1%")
    trade.setdefault("stop_loss", "2% below entry")
    trade.setdefault("target", "4% above entry")

    data.setdefault("symbol", req.symbol)
    data.setdefault("horizon", req.horizon)
    data.setdefault("bias", "neutral")
    data.setdefault("summary", "No clear edge detected.")
    data.setdefault("reasons", [])
    data.setdefault("risks", [])
    data["trade_idea"] = trade

    return data

@app.get("/api/price-data")
def price_data(symbol: str, horizon: Optional[str] = "1"):
    return {
        "prices": get_price_series(symbol, horizon)
    }