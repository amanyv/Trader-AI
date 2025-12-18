from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

QDRANT_HOST = "qdrant"
QDRANT_PORT = 6333
COLLECTION = "market_docs"

client = QdrantClient(
    url=f"http://{QDRANT_HOST}:{QDRANT_PORT}"
)

def ensure_collection(vector_size: int):
    collections = client.get_collections().collections
    names = [c.name for c in collections]

    if COLLECTION not in names:
        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )
