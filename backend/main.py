import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware    
from typing import Optional
from dotenv import load_dotenv
from uuid import UUID, uuid4
from contextlib import asynccontextmanager

from database import create_chat_history_table, save_chat_history
from qdrant_service import QdrantClientService
from openai_service import OpenAIService

# Load environment variables from .env file
load_dotenv()

# --- Application Lifespan --- #
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    print("Starting up FastAPI application...")
    try:
        create_chat_history_table()
        print("Chat history table checked/created successfully.")
    except Exception as e:
        print(f"Failed to create chat history table on startup: {e}")
        # Depending on criticality, you might want to raise here or log and continue
    yield
    # Shutdown event
    print("Shutting down FastAPI application.")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
try:
    openai_service = OpenAIService()
    qdrant_service = QdrantClientService()
except ValueError as e:
    print(f"Environment variable error during service initialization: {e}")
    exit(1) # Exit if essential env vars are missing
except Exception as e:
    print(f"Error initializing services: {e}")
    exit(1)


class ChatMessage(BaseModel):
    message: str
    selected_context: Optional[str] = None


@app.post("/chat")
async def chat(message: ChatMessage):
    try:
        # 1. Get embedding for user message
        user_embedding = openai_service.get_embedding(message.message)

        # 2. Search Qdrant for relevant book knowledge
        retrieved_chunks = qdrant_service.search_book_knowledge(user_embedding)
        retrieved_chunks_content = "\n".join(retrieved_chunks)

        # 3. Construct the RAG prompt
        rag_prompt_parts = [
            "Use the following context from the book to answer the question:\n\nContext:"
        ]
        if message.selected_context:
            rag_prompt_parts.append(f"{message.selected_context}")
        if retrieved_chunks_content:
            rag_prompt_parts.append(f"{retrieved_chunks_content}")

        rag_prompt_parts.append(f"\nQuestion:\n{message.message}\n\nProvide a concise answer based on the provided context.")

        rag_prompt = "\n".join(rag_prompt_parts)

        # 4. Generate response using OpenAI
        bot_response = openai_service.generate_response(rag_prompt)

        # 5. Generate conversation_id and save chat history
        conversation_id = uuid4()
        try:
            save_chat_history(
                conversation_id=str(conversation_id),
                user_message=message.message,
                bot_response=bot_response,
                selected_text=message.selected_context,
            )
        except Exception as db_error:
            print(f"⚠️ Warning: Database save failed, but continuing. Error: {db_error}")

        return {"reply": bot_response, "conversation_id": str(conversation_id)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
# ... imports
import qdrant_client
# ... existing imports

# ... (inside chat function exception handler)
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"❌ Critical Error: {error_details}")
        
        # Debugging info for Vercel
        try:
            client_version = qdrant_client.__version__
            client_attrs = dir(qdrant_service.client) if qdrant_service and hasattr(qdrant_service, 'client') else "Client not initialized"
        except:
            client_version = "unknown"
            client_attrs = "error getting attrs"

        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)} | Qdrant Version: {client_version} | Client Attrs: {str(client_attrs)[:200]}...")

# Example of a simple root endpoint (optional, for testing if the server is running)
@app.get("/")
async def read_root():
    return {"message": "RAG Chatbot Backend is running!"}
