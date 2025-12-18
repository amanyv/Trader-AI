from backend.agents.technical_agent import TechnicalAgent
from backend.agents.news_agent import NewsAgent
from backend.agents.macro_agent import MacroAgent
from backend.agents.risk_agent import RiskAgent
from backend.agents.synthesis_agent import SynthesisAgent

class SymbolAnalysisOrchestrator:
    async def run(self, symbol: str, horizon: str) -> dict:
        technical = TechnicalAgent().run(symbol)
        news = await NewsAgent().run(symbol)
        macro = await MacroAgent().run()
        risk = RiskAgent().evaluate(technical, news, macro)

        result = await SynthesisAgent().run(
            symbol, horizon, technical, news, macro, risk
        )

        # Deterministic override (FINAL GUARDRAIL)
        if not risk["allow_trade"]:
            result["trade_idea"]["direction"] = "no_trade"

        return result
