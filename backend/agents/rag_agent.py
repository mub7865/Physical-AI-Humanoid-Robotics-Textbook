from openai import OpenAI
from typing import Dict, List, Any
import os
import sys
from pathlib import Path

# Add the parent directory to sys.path to allow importing from the parent directory
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from qdrant_service import QdrantClientService
from openai_service import OpenAIService


class RAGAgent:
    """
    RAG Agent that handles document retrieval and context composition using OpenAI Assistants API
    """

    def __init__(self):
        self.client = OpenAIService().client  # Use the OpenAI client from our existing service
        self.qdrant_service = QdrantClientService()
        self.openai_service = OpenAIService()

    def search_tool(self, query: str) -> str:
        """
        Search the textbook content for relevant information
        """
        try:
            # Get embedding for the query using our existing service
            query_embedding = self.openai_service.get_embedding(query)

            # Search Qdrant for relevant chunks
            retrieved_chunks = self.qdrant_service.search_book_knowledge(query_embedding)
            retrieved_chunks_content = "\n".join(retrieved_chunks)

            return retrieved_chunks_content
        except Exception as e:
            return f"Error during search: {str(e)}"

    def process_query(self, query: str, selected_context: str = None) -> str:
        """
        Process a user query using RAG approach
        """
        # First, search for relevant information
        retrieved_content = self.search_tool(query)

        # Construct the prompt with retrieved content and selected context
        rag_prompt_parts = [
            "You are an expert assistant for the Physical AI & Humanoid Robotics textbook. Use the provided context to answer the user's question accurately."
        ]

        if selected_context:
            rag_prompt_parts.append(f"\nSelected Text Context:\n{selected_context}")

        if retrieved_content:
            rag_prompt_parts.append(f"\nRAG Retrieved Content:\n{retrieved_content}")

        rag_prompt_parts.append(f"\nQuestion:\n{query}\n\nProvide a comprehensive, accurate answer based on the provided context.")

        rag_prompt = "\n".join(rag_prompt_parts)

        # Generate response using OpenAI - using our existing service method
        response = self.openai_service.generate_response(rag_prompt)

        return response