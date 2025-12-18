from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.agents.orchestrator import SymbolAnalysisOrchestrator
from backend.evaluation.store import save_analysis
from backend.storage.db import init_db

# -------------------------
# Initialize DB
# -------------------------
init_db()

# -------------------------
# Create FastAPI app FIRST
# -------------------------
app = FastAPI(title="TraderGPT Pro")

# -------------------------
# API models
# -------------------------
class AnalyzeRequest(BaseModel):
    symbol: str
    horizon: str

# -------------------------
# API routes
# -------------------------
@app.post("/api/analyze-symbol")
async def analyze(req: AnalyzeRequest):
    try:
        print("STEP 1: endpoint hit")

        orchestrator = SymbolAnalysisOrchestrator()
        print("STEP 2: orchestrator created")

        result = await orchestrator.run(req.symbol, req.horizon)
        print("STEP 3: orchestrator completed")

        return result

    except Exception as e:
        # 🔥 CRITICAL: never crash the UI
        print("ANALYZE ERROR:", repr(e))

        return {
            "symbol": req.symbol,
            "horizon": req.horizon,
            "bias": "neutral",
            "summary": "AI analysis temporarily unavailable. Showing fallback response.",
            "reasons": [
                "Backend safety fallback triggered",
                "RAG / agent pipeline encountered an error"
            ],
            "risks": [
                "This is a placeholder response",
                "Backend logs should be checked"
            ],
            "trade_idea": {
                "direction": "long",
                "entry_zone": "N/A",
                "stop_loss": "N/A",
                "target": "N/A",
                "notes": "Fallback mode"
            },
            "sources": []
        }



@app.get("/api/metrics")
def metrics():
    return {"status": "ok"}  # simple check for now

# -------------------------
# Mount frontend LAST
# -------------------------
app.mount(
    "/",
    StaticFiles(directory="/app/backend/static", html=True),
    name="static",
)
