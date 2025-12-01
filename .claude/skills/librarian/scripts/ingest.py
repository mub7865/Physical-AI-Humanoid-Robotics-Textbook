import os
from openai import OpenAI
from qdrant_client import QdrantClient, models
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
qdrant_client = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))

COLLECTION_NAME = "book_content"

def get_embeddings(text):
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-3-small" # or another suitable model
    )
    return response.data[0].embedding

def ingest_document(document_id, content, metadata=None):
    embedding = get_embeddings(content)
    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            models.PointStruct(
                id=document_id,
                vector=embedding,
                payload={"content": content, **(metadata or {})}
            )
        ]
    )
    print(f"Document {document_id} ingested into Qdrant.")

if __name__ == "__main__":
    # Example: Initialize collection (run once)
    # qdrant_client.recreate_collection(
    #     collection_name=COLLECTION_NAME,
    #     vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
    # )

    sample_content = "This is a sample paragraph about AI-Native books."
    ingest_document("sample_doc_1", sample_content, {"source": "test_ingest"})