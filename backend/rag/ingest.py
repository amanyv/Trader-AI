import asyncio
from backend.openrouter import embed_text
from backend.rag.vector_store import client, COLLECTION, init_collection

docs = [
    {
        "id": 1,
        "symbol": "RELIANCE",
        "content": "Reliance Industries shows strong weekly support near 2450 with positive momentum."
    },
    {
        "id": 2,
        "symbol": "RELIANCE",
        "content": "Retail and Jio segments continue to provide earnings stability."
    },
    {
        "id": 3,
        "symbol": "RELIANCE",
        "content": "Overall market sentiment remains neutral to slightly bullish for large-cap stocks."
    }
]

async def ingest():
    test_vec = await embed_text("test")
    init_collection(len(test_vec))

    points = []
    for d in docs:
        vec = await embed_text(d["content"])
        points.append({
            "id": d["id"],
            "vector": vec,
            "payload": d
        })

    client.upsert(collection_name=COLLECTION, points=points)

asyncio.run(ingest())
print("✅ Documents ingested into Qdrant")
