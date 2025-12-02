import os
from openai import OpenAI
import httpx
from typing import List

class OpenAIService:
    def __init__(self):
        self.client = self._initialize_openai_client()

    def _initialize_openai_client(self) -> OpenAI:
        """Initializes the OpenAI client using the environment variable."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        try:
            return OpenAI(api_key=api_key, http_client=httpx.Client())
        except Exception as e:
            print(f"Error initializing OpenAI client: {e}")
            raise

    def get_embedding(self, text: str) -> List[float]:
        """Generates an embedding for the given text using text-embedding-3-small."""
        try:
            text = text.replace("\n", " ")
            response = self.client.embeddings.create(input=[text], model="text-embedding-3-small")
            return response.data[0].embedding
        except Exception as e:
            print(f"Error getting embedding from OpenAI: {e}")
            raise

    def generate_response(self, prompt: str) -> str:
        """Generates a response using gpt-4o-mini."""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating response from OpenAI: {e}")
            raise
