import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from dotenv import load_dotenv
from uuid import UUID, uuid4
from contextlib import asynccontextmanager
import qdrant_client

from database import create_chat_history_table, save_chat_history
from agents.conversation_agent import ConversationAgent

# Load environment variables from .env file
load_dotenv()

# --- Application Lifespan --- #
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    print("Starting up FastAPI application with Agent framework...")
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

# Initialize Agent
try:
    conversation_agent = ConversationAgent()
except ValueError as e:
    print(f"Environment variable error during agent initialization: {e}")
    exit(1) # Exit if essential env vars are missing
except Exception as e:
    print(f"Error initializing agent: {e}")
    exit(1)


class ChatMessage(BaseModel):
    message: str
    selected_context: Optional[str] = None


@app.post("/chat")
async def chat(message: ChatMessage):
    try:
        # Process message through the conversation agent
        bot_response = conversation_agent.process_message(
            message=message.message,
            selected_context=message.selected_context
        )

        # Generate conversation_id and save chat history
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
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"❌ Critical Error: {error_details}")

        # Debugging info
        try:
            agent_info = f"Agent initialized: {conversation_agent is not None}"
        except:
            agent_info = "error getting agent info"

        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)} | Agent Info: {agent_info}")

# Example of a simple root endpoint (optional, for testing if the server is running)
@app.get("/")
async def read_root():
    return {"message": "RAG Chatbot Backend is running!"}