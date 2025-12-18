from typing import Optional
from pydantic import BaseModel

class AnalysisRecord(BaseModel):
    id: str
    symbol: str
    horizon: str
    bias: str
    confidence: int
    risk_reward: str
    summary: str
    trade_json: str
    created_at: str
    outcome: Optional[str] = None
