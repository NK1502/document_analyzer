import os
import time

try:
    from pinecone import Pinecone, ServerlessSpec
except Exception as exc:
    Pinecone = None
    ServerlessSpec = None
    PINECONE_IMPORT_ERROR = exc
else:
    PINECONE_IMPORT_ERROR = None

INDEX_NAME = "ai-doc-analyzer-index"
EMBEDDING_DIMENSION = 768

pinecone_client = None

def _require_pinecone_sdk():
    if Pinecone is None or ServerlessSpec is None:
        raise RuntimeError(
            "The Pinecone SDK is not available. Run `pip install pinecone` in the backend environment."
        ) from PINECONE_IMPORT_ERROR

def _require_api_key() -> str:
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        raise RuntimeError("PINECONE_API_KEY is missing. Add it to backend/.env before uploading documents.")
    return api_key

def get_pinecone_index():
    global pinecone_client
    _require_pinecone_sdk()

    if not pinecone_client:
        pinecone_client = Pinecone(api_key=_require_api_key())
    
    if INDEX_NAME not in pinecone_client.list_indexes().names():
        pinecone_client.create_index(
            name=INDEX_NAME,
            dimension=EMBEDDING_DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1",
            ),
        )

        while not pinecone_client.describe_index(INDEX_NAME).status["ready"]:
            time.sleep(1)

    return pinecone_client.Index(INDEX_NAME)

def upsert_vectors(vectors):
    """
    vectors should be a list of dicts: [{"id": "chunk_id", "values": [0.1, 0.2...], "metadata": {"text": "chunk text"}}]
    """
    index = get_pinecone_index()
    # Upsert in batches of 100 to avoid limits
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        index.upsert(vectors=vectors[i:i + batch_size])

def query_vectors(query_embedding, document_id: str, top_k=3):
    """Queries pinecone for the most similar chunks."""
    index = get_pinecone_index()
    return index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        filter={"document_id": {"$eq": document_id}},
    )
