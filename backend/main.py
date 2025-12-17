import os
from dotenv import load_dotenv

# Load environment variables FIRST before any other imports that use them
load_dotenv()

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from uuid import UUID, uuid4
from contextlib import asynccontextmanager
import qdrant_client

from database import create_chat_history_table, save_chat_history, init_all_tables, clear_user_cache
from agents.conversation_agent import ConversationAgent
from auth import auth_router, profile_router, get_current_user, get_optional_user
from services import PersonalizationService, TranslationService

# --- Application Lifespan --- #
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    print("Starting up FastAPI application with Agent framework...")
    try:
        # Initialize all database tables (users, profiles, sessions, cache, chat_history)
        init_all_tables()
        print("All database tables checked/created successfully.")
    except Exception as e:
        print(f"Failed to initialize database tables on startup: {e}")
        # Depending on criticality, you might want to raise here or log and continue
    yield
    # Shutdown event
    print("Shutting down FastAPI application.")


app = FastAPI(
    title="Physical AI & Humanoid Robotics Textbook API",
    description="RAG-powered chatbot with user authentication and content personalization",
    version="2.0.0",
    lifespan=lifespan
)

# Register auth routes (T021)
app.include_router(auth_router)
app.include_router(profile_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://mub7865.github.io",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
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


# ============================================
# T033: Personalization Endpoints
# ============================================
personalization_service = PersonalizationService()
translation_service = TranslationService()


class PersonalizeRequest(BaseModel):
    chapter_id: str
    content: str = Field(..., max_length=50000)  # 50KB limit
    use_cache: bool = True


class TranslateRequest(BaseModel):
    chapter_id: str
    content: str = Field(..., max_length=50000)  # 50KB limit
    target_language: str = "roman_urdu"
    use_cache: bool = True


class CacheClearRequest(BaseModel):
    chapter_id: Optional[str] = None


@app.post("/api/personalize")
async def personalize_content(
    request: PersonalizeRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    T033: Personalize chapter content based on user's background profile.
    Requires authentication.
    """
    try:
        result = personalization_service.personalize_content(
            user_id=str(current_user["id"]),
            chapter_id=request.chapter_id,
            content=request.content,
            use_cache=request.use_cache
        )
        return result
    except ValueError as e:
        error_code = str(e)
        if error_code == "PROFILE_NOT_FOUND":
            raise HTTPException(
                status_code=404,
                detail={"error": "PROFILE_NOT_FOUND", "message": "User profile required for personalization"}
            )
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        error_msg = str(e)
        if "AI_SERVICE_ERROR" in error_msg:
            raise HTTPException(
                status_code=503,
                detail={"error": "AI_SERVICE_ERROR", "message": "OpenAI API temporarily unavailable"}
            )
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/personalize/cache")
async def clear_personalization_cache(
    request: CacheClearRequest,
    current_user: dict = Depends(get_current_user)
):
    """Clear personalized content cache for current user."""
    try:
        count = clear_user_cache(str(current_user["id"]), request.chapter_id)
        return {"message": "Cache cleared successfully", "chapters_cleared": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================
# T041: Translation Endpoints
# ============================================
@app.post("/api/translate")
async def translate_content(
    request: TranslateRequest,
    current_user: Optional[dict] = Depends(get_optional_user)
):
    """
    T041: Translate chapter content to Roman Urdu.
    Works for both authenticated and guest users.
    """
    try:
        result = translation_service.translate_content(
            chapter_id=request.chapter_id,
            content=request.content,
            target_language=request.target_language,
            use_cache=request.use_cache,
            user_id=str(current_user["id"]) if current_user else None
        )
        return result
    except ValueError as e:
        error_code = str(e)
        if error_code == "UNSUPPORTED_LANGUAGE":
            raise HTTPException(
                status_code=400,
                detail={"error": "UNSUPPORTED_LANGUAGE", "message": "Only roman_urdu is supported"}
            )
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        error_msg = str(e)
        if "AI_SERVICE_ERROR" in error_msg:
            raise HTTPException(
                status_code=503,
                detail={"error": "AI_SERVICE_ERROR", "message": "OpenAI API temporarily unavailable"}
            )
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/translate/languages")
async def get_supported_languages():
    """Get list of supported translation languages."""
    return TranslationService.get_supported_languages()