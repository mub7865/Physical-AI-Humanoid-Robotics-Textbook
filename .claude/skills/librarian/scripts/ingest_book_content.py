import os
import glob
from uuid import uuid4
from openai import OpenAI
from qdrant_client import QdrantClient, models
from dotenv import load_dotenv
import httpx

load_dotenv(dotenv_path="/mnt/d/AI-DRIVEN_AND_SPEC-DRIVEN_HACKATHON(Failde)/backend/.env")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), http_client=httpx.Client())
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

# Base path for book documentation
BOOK_DOCS_PATH = "/mnt/d/AI-DRIVEN_AND_SPEC-DRIVEN_HACKATHON(Failde)/book/docs/"

def chunk_markdown_by_headings(markdown_content: str, file_path: str) -> list[dict]:
    """Chunks markdown content into sections based on headings."""
    chunks = []
    current_chunk_content = []
    current_heading = "Document Start" # Default for content before first heading
    chunk_id_counter = 0

    lines = markdown_content.splitlines()
    for line in lines:
        # Detect headings
        if line.startswith("#"):
            if current_chunk_content: # Save previous chunk
                chunks.append({
                    "id": f"{file_path}-{chunk_id_counter}",
                    "content": "\n".join(current_chunk_content).strip(),
                    "metadata": {"source_file": file_path, "heading": current_heading}
                })
                chunk_id_counter += 1
                current_chunk_content = []
            current_heading = line.strip()
            current_chunk_content.append(line)
        else:
            current_chunk_content.append(line)

    if current_chunk_content: # Save the last chunk
        chunks.append({
            "id": f"{file_path}-{chunk_id_counter}",
            "content": "\n".join(current_chunk_content).strip(),
            "metadata": {"source_file": file_path, "heading": current_heading}
        })
    return chunks

def ingest_book_content():
    """Reads Markdown files, chunks content, and ingests into Qdrant."""
    markdown_files = glob.glob(os.path.join(BOOK_DOCS_PATH, "**/*.md"), recursive=True)
    print(f"Found {len(markdown_files)} Markdown files to ingest.")

    for file_path in markdown_files:
        print(f"Processing file: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            chunks = chunk_markdown_by_headings(content, file_path)

            for chunk in chunks:
                # Use a UUID for document_id to ensure uniqueness across files/chunks
                # You can also use a hash of content or a combination of file_path and chunk_id
                doc_id = str(uuid4()) # Generate unique ID for each chunk
                ingest_document(doc_id, chunk["content"], chunk["metadata"])

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    ingest_book_content()