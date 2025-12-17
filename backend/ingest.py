import os
import glob
from typing import List
from uuid import uuid4
from dotenv import load_dotenv
from qdrant_client.http.models import PointStruct

# Import services - assuming running from backend directory
from openai_service import OpenAIService
from qdrant_service import QdrantClientService

load_dotenv()

def load_documents(docs_path: str) -> List[dict]:
    documents = []
    # Recursively find all .md files
    for root, _, files in os.walk(docs_path):
        for file in files:
            if file.endswith(".md") or file.endswith(".mdx"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    documents.append({
                        "path": file_path,
                        "content": content,
                        "filename": file
                    })
    return documents

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Simple chunking by character count with overlap."""
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - overlap)
    return chunks

def main():
    print("Initializing services...")
    try:
        openai_service = OpenAIService()
        qdrant_service = QdrantClientService()
    except Exception as e:
        print(f"Failed to initialize services: {e}")
        return

    # Resolve path relative to this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    docs_path = os.path.abspath(os.path.join(current_dir, "../book/docs"))
    
    print(f"Loading documents from {docs_path}...")
    if not os.path.exists(docs_path):
        print(f"Error: Documents directory not found at {docs_path}")
        return

    documents = load_documents(docs_path)
    print(f"Found {len(documents)} documents.")

    all_points = []
    total_chunks = 0

    print("Processing documents...")
    for doc in documents:
        chunks = chunk_text(doc["content"])
        for chunk in chunks:
            try:
                embedding = openai_service.get_embedding(chunk)
                point = PointStruct(
                    id=str(uuid4()),
                    vector=embedding,
                    payload={
                        "content": chunk,
                        "source": doc["path"],
                        "filename": doc["filename"]
                    }
                )
                all_points.append(point)
                total_chunks += 1
                print(f"Processed chunk {total_chunks} for {doc['filename']}", end="\r")
            except Exception as e:
                print(f"\nError processing chunk for {doc['filename']}: {e}")

    print(f"\nUploading {len(all_points)} chunks to Qdrant...")
    if all_points:
        try:
            # Upload in smaller batches to avoid timeout
            batch_size = 20
            for i in range(0, len(all_points), batch_size):
                batch = all_points[i : i + batch_size]
                qdrant_service.client.upsert(
                    collection_name=qdrant_service.collection_name,
                    points=batch,
                    wait=True
                )
                print(f"Uploaded batch {i // batch_size + 1}/{(len(all_points) + batch_size - 1) // batch_size}")
            print("Ingestion complete!")
        except Exception as e:
            print(f"Error uploading to Qdrant: {e}")
    else:
        print("No content to upload.")

if __name__ == "__main__":
    main()
