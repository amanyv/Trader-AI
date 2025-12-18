from backend.rag.retrieve import get_context

class MacroAgent:
    async def run(self) -> dict:
        context = await get_context("India macro interest rates market sentiment")
        return {
            "macro_context": context,
            "regime": "risk-on" if context else "neutral"
        }
