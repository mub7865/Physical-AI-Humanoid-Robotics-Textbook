import os
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from typing import List

class QdrantClientService:
    def __init__(self):
        self.collection_name = "book_content"
        self.client = self._initialize_qdrant_client()

    def _initialize_qdrant_client(self) -> QdrantClient:
        """Initializes the Qdrant client using environment variables."""
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_api_key = os.getenv("QDRANT_API_KEY")

        if not qdrant_url:
            raise ValueError("QDRANT_URL environment variable not set.")

        try:
            client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
            # Ensure the collection exists, or create it. This assumes a fixed vector size for embeddings.
            # The embedding model 'text-embedding-3-small' typically produces 1536-dimensional vectors.
            try:
                client.get_collection(collection_name=self.collection_name)
            except Exception:
                print(f"Collection {self.collection_name} not found, creating it.")
                client.recreate_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=1536, distance=Distance.COSINE),
                )
            return client
        except Exception as e:
            print(f"Error initializing Qdrant client: {e}")
            raise

    def search_book_knowledge(self, query_embedding: List[float]) -> List[str]:
        """Searches the book_knowledge collection for the top 3 matching chunks."""
        try:
            search_result = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=3,
                with_payload=True,
            )
            # Extract the 'content' from the payload of each search result
            chunks = [hit.payload['content'] for hit in search_result if 'content' in hit.payload]
            return chunks
        except Exception as e:
            print(f"Error searching Qdrant: {e}")
            raise
