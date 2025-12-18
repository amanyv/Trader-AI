from backend.rag.retrieve import get_context

class NewsAgent:
    async def run(self, symbol: str) -> dict:
        context = await get_context(f"{symbol} recent news earnings sentiment")
        return {
            "news_context": context,
            "sentiment": "positive" if context else "neutral"
        }
