from backend.rag.vector_store import client, COLLECTION, ensure_collection
from backend.openrouter import embed_text

_seeded = False

async def ensure_seed_data():
    global _seeded
    if _seeded:
        return

    test_vec = await embed_text("seed")
    ensure_collection(len(test_vec))

    _seeded = True


async def get_context(query: str, top_k: int = 3) -> str:
    """
    Temporary safe RAG stub.
    Keeps architecture intact but avoids Qdrant runtime failures.
    """
    return ""
