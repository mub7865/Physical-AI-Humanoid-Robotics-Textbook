
---
id: 0007
title: Implement RAG Chatbot Backend Feature
stage: general
date: 2025-12-02
surface: agent
feature: none
branch: main
user: |-
  Implement the RAG Chatbot Backend feature based on the **updated tasks** outlined in `specs/006-rag-chatbot-backend/tasks.md` and the **approved updated plan** in `specs/006-rag-chatbot-backend/plan.md`.

  **Key Implementation Steps (as per `tasks.md`):**

  1.  **Setup:**
      -   Create the `backend/` directory if it doesn't exist.
      -   Create `backend/requirements.txt` and add the specified Python dependencies.

  2.  **Database (`backend/database.py`):**
      -   Implement functions to connect to Neon Postgres using the `NEON_DB_URL` environment variable.
      -   Implement a function `create_chat_history_table()` to create the `chat_history` table if it doesn't exist. **The table schema must include the `selected_text` column as `TEXT NULLABLE`**:
          -   `conversation_id` (UUID PRIMARY KEY)
          -   `user_message` (TEXT NOT NULL)
          -   `bot_response` (TEXT NOT NULL)
          -   `selected_text` (TEXT NULLABLE)
          -   `timestamp` (TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL)
      -   Implement a function `save_chat_history(conversation_id: UUID, user_message: str, bot_response: str, selected_text: Optional[str])` to insert conversation data, including `selected_text`, into the `chat_history` table.

  3.  **Vector DB (`backend/qdrant_client.py`):**
      -   Implement a class `QdrantClientService`.
      -   Initialize the Qdrant client using `QDRANT_URL` and `QDRANT_API_KEY` (if applicable) environment variables.
      -   Implement a method `search_book_knowledge(query_embedding: list[float]) -> list[str]` that searches the `book_knowledge` collection for the top 3 matching chunks and returns their content.

  4.  **OpenAI Service (`backend/openai_service.py`):**
      -   Implement a class `OpenAIService`.
      -   Initialize the OpenAI client using `OPENAI_API_KEY` environment variable.
      -   Implement a method `get_embedding(text: str) -> list[float]` to embed text using `text-embedding-3-small`.
      -   Implement a method `generate_response(prompt: str) -> str` to generate a response using `gpt-4o-mini`.

  5.  **FastAPI Application (`backend/main.py`):**
      -   Initialize the FastAPI application.
      -   Load environment variables using `python-dotenv`.
      -   Define a Pydantic model `ChatMessage` for the POST request body (`user_message: str`, `selected_text: Optional[str]`).
      -   Implement the POST `/chat` endpoint:
          -   Receive `user_message` and `selected_text` from the request body.
          -   Call `OpenAIService.get_embedding()` to get the embedding of `user_message`.
          -   Call `QdrantClientService.search_book_knowledge()` with the embedding to retrieve relevant chunks.
          -   **Construct the RAG prompt according to the clarified logic:**
              ```
              Use the following context from the book to answer the question:

              Context:
              {selected_text_if_available}
              {retrieved_chunks_content}

              Question:
              {user_message}

              Provide a concise answer based on the provided context.
              ```
              (Where `{selected_text_if_available}` is included *only if `selected_text` is not None*, and is placed *before* `{retrieved_chunks_content}`.)
          -   Call `OpenAIService.generate_response()` with the constructed prompt to get `bot_response`.
          -   Generate a `conversation_id` (UUID).
          -   Call `database.save_chat_history()` to store the conversation, including `selected_text`.
          -   Return a JSON response with `{"response": bot_response, "conversation_id": str(conversation_id)}`.

  **Environment Variables:** Ensure all API keys and URLs (`NEON_DB_URL`, `QDRANT_URL`, `QDRANT_API_KEY` (if used), `OPENAI_API_KEY`) are loaded from `.env`.

  **Error Handling:** Implement basic exception handling for API calls (OpenAI, Qdrant, Postgres) and return appropriate HTTP 400 or 500 errors. Each service should handle its own connection/client initialization and error handling.

  **Modular Structure:** Maintain the modular structure with separate files for database, Qdrant, OpenAI, and main FastAPI application logic.
response: ""
command: ""
labels: ["RAG", "Backend", "FastAPI", "OpenAI", "Qdrant", "Postgres"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - /mnt/d/AI-DRIVEN_AND_SPEC-DRIVEN_HACKATHON/history/prompts/general/0007-implement-rag-chatbot-backend-feature.general.prompt.md
tests_yaml: |
  - None
outcome: PHR created successfully.
evaluation: -

---

```
# Implement RAG Chatbot Backend Feature

## User Prompt
Implement the RAG Chatbot Backend feature based on the **updated tasks** outlined in `specs/006-rag-chatbot-backend/tasks.md` and the **approved updated plan** in `specs/006-rag-chatbot-backend/plan.md`.

**Key Implementation Steps (as per `tasks.md`):**

1.  **Setup:**
    -   Create the `backend/` directory if it doesn't exist.
    -   Create `backend/requirements.txt` and add the specified Python dependencies.

2.  **Database (`backend/database.py`):**
    -   Implement functions to connect to Neon Postgres using the `NEON_DB_URL` environment variable.
    -   Implement a function `create_chat_history_table()` to create the `chat_history` table if it doesn't exist. **The table schema must include the `selected_text` column as `TEXT NULLABLE`**:
        -   `conversation_id` (UUID PRIMARY KEY)
        -   `user_message` (TEXT NOT NULL)
        -   `bot_response` (TEXT NOT NULL)
        -   `selected_text` (TEXT NULLABLE)
        -   `timestamp` (TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL)
    -   Implement a function `save_chat_history(conversation_id: UUID, user_message: str, bot_response: str, selected_text: Optional[str])` to insert conversation data, including `selected_text`, into the `chat_history` table.

3.  **Vector DB (`backend/qdrant_client.py`):**
    -   Implement a class `QdrantClientService`.
    -   Initialize the Qdrant client using `QDRANT_URL` and `QDRANT_API_KEY` (if applicable) environment variables.
    -   Implement a method `search_book_knowledge(query_embedding: list[float]) -> list[str]` that searches the `book_knowledge` collection for the top 3 matching chunks and returns their content.

4.  **OpenAI Service (`backend/openai_service.py`):**
    -   Implement a class `OpenAIService`.
    -   Initialize the OpenAI client using `OPENAI_API_KEY` environment variable.
    -   Implement a method `get_embedding(text: str) -> list[float]` to embed text using `text-embedding-3-small`.
    -   Implement a method `generate_response(prompt: str) -> str` to generate a response using `gpt-4o-mini`.

5.  **FastAPI Application (`backend/main.py`):**
    -   Initialize the FastAPI application.
    -   Load environment variables using `python-dotenv`.
    -   Define a Pydantic model `ChatMessage` for the POST request body (`user_message: str`, `selected_text: Optional[str]`).
    -   Implement the POST `/chat` endpoint:
        -   Receive `user_message` and `selected_text` from the request body.
        -   Call `OpenAIService.get_embedding()` to get the embedding of `user_message`.
        -   Call `QdrantClientService.search_book_knowledge()` with the embedding to retrieve relevant chunks.
        -   **Construct the RAG prompt according to the clarified logic:**
            ```
            Use the following context from the book to answer the question:

            Context:
            {selected_text_if_available}
            {retrieved_chunks_content}

            Question:
            {user_message}

            Provide a concise answer based on the provided context.
            ```
            (Where `{selected_text_if_available}` is included *only if `selected_text` is not None*, and is placed *before* `{retrieved_chunks_content}`.)
        -   Call `OpenAIService.generate_response()` with the constructed prompt to get `bot_response`.
        -   Generate a `conversation_id` (UUID).
        -   Call `database.save_chat_history()` to store the conversation, including `selected_text`.
        -   Return a JSON response with `{"response": bot_response, "conversation_id": str(conversation_id)}`.

**Environment Variables:** Ensure all API keys and URLs (`NEON_DB_URL`, `QDRANT_URL`, `QDRANT_API_KEY` (if used), `OPENAI_API_KEY`) are loaded from `.env`.

**Error Handling:** Implement basic exception handling for API calls (OpenAI, Qdrant, Postgres) and return appropriate HTTP 400 or 500 errors. Each service should handle its own connection/client initialization and error handling.

**Modular Structure:** Maintain the modular structure with separate files for database, Qdrant, OpenAI, and main FastAPI application logic.

## Assistant Response

```
I will implement the RAG Chatbot Backend feature by creating the necessary Python files in the `backend/` directory, setting up dependencies, and defining the FastAPI endpoint for chat, ensuring the integration of OpenAI for embeddings and response generation, Qdrant for vector search, and Neon Postgres for chat history, including the `selected_text` column.

Constraints, Invariants, Non-Goals:
*   **Constraints:** All environment variables must be loaded from `.env`. Only the Pure OpenAI SDK will be used. FastAPI endpoints must handle `user_message` and `selected_text`. The chat history table must include `selected_text TEXT NULLABLE`.
*   **Invariants:** The RAG prompt structure must be exactly as specified. Dependencies in `requirements.txt` are accurate and compatible.
*   **Non-Goals:** Frontend implementation, advanced authentication beyond API keys, complex error handling beyond basic try-except blocks, or detailed logging configurations are outside the scope of this task.

I will start by creating the PHR.
```
