import json
from backend.openrouter import llm_complete

class SynthesisAgent:
    async def run(
        self,
        symbol: str,
        horizon: str,
        technical: dict,
        news: dict,
        macro: dict,
        risk: dict
    ) -> dict:

        system_prompt = f"""
You are TraderGPT Pro.

Use the following structured inputs.
DO NOT invent facts beyond them.

TECHNICAL:
{technical}

NEWS:
{news["news_context"]}

MACRO:
{macro["macro_context"]}

RISK CONSTRAINTS:
confidence_score={risk["confidence_score"]}
risk_reward_ratio={risk["risk_reward_ratio"]}
allow_trade={risk["allow_trade"]}

Return JSON ONLY in this schema:

{{
  "symbol": "{symbol}",
  "horizon": "{horizon}",
  "bias": "...",
  "confidence_score": {risk["confidence_score"]},
  "risk_reward_ratio": "{risk["risk_reward_ratio"]}",
  "summary": "...",
  "reasons": [],
  "risks": [],
  "trade_idea": {{
    "direction": "long|short|no_trade",
    "entry_zone": "",
    "stop_loss": "",
    "target": "",
    "notes": ""
  }}
}}
"""

        user_prompt = "Generate final trade analysis respecting all constraints."

        raw = await llm_complete([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ])

        return json.loads(raw)
