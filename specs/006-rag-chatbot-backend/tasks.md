# Task Checklist: RAG Chatbot Backend (Updated for Selected Text)

Yeh document RAG Chatbot Backend ko implement karne ke liye detailed tasks outline karta hai, jo ki updated specification aur plan par based hai. Khaas taur par, `selected_text` functionality ko shamil kiya gaya hai.

## Implementation Tasks

1.  [ ] **Setup:** `backend/` folder aur `requirements.txt` create karna, jismein yeh Python dependencies shamil honge:
    -   `fastapi`
    -   `uvicorn`
    -   `openai`
    -   `qdrant-client`
    -   `psycopg2-binary`
    -   `python-dotenv`
2.  [ ] **Database Initialization:** `backend/database.py` create karna:
    -   `NEON_DB_URL` environment variable use karke Neon Postgres se connection establish karna.
    -   `create_chat_history_table()` function implement karna, jo `chat_history` table ko create karega agar woh exist nahi karta. Table schema mein `conversation_id` (UUID PRIMARY KEY), `user_message` (TEXT), `bot_response` (TEXT), `selected_text` (TEXT NULLABLE), aur `timestamp` (TIMESTAMP WITH TIME ZONE DEFAULT NOW()) columns honge.
    -   `save_chat_history(conversation_id: UUID, user_message: str, bot_response: str, selected_text: Optional[str])` function implement karna, jo conversation data ko `chat_history` table mein insert karega.
3.  [ ] **Vector Database Client:** `backend/qdrant_client.py` create karna:
    -   `QdrantClientService` class implement karna.
    -   `QDRANT_URL` aur `QDRANT_API_KEY` (agar applicable ho) environment variables use karke Qdrant client initialize karna.
    -   `search_book_knowledge(query_embedding: list[float]) -> list[str]` method implement karna, jo `book_knowledge` collection mein top 3 matching chunks ko search karega aur unka content return karega.
4.  [ ] **OpenAI Service:** `backend/openai_service.py` create karna:
    -   `OpenAIService` class implement karna.
    -   `OPENAI_API_KEY` environment variable use karke OpenAI client initialize karna.
    -   `get_embedding(text: str) -> list[float]` method implement karna, jo `text-embedding-3-small` use karke text ko embed karega.
    -   `generate_response(prompt: str) -> str` method implement karna, jo `gpt-4o-mini` use karke response generate karega.
5.  [ ] **FastAPI Application:** `backend/main.py` create karna:
    -   FastAPI application initialize karna.
    -   `python-dotenv` use karke environment variables load karna.
    -   `ChatMessage` Pydantic model define karna POST request body ke liye, jismein `user_message: str` aur `selected_text: Optional[str]` honge.
    -   POST `/chat` endpoint implement karna:
        -   Request body se `user_message` aur `selected_text` receive karna.
        -   `OpenAIService.get_embedding()` call karke `user_message` ka embedding lena.
        -   `QdrantClientService.search_book_knowledge()` call karke relevant book chunks retrieve karna.
        -   RAG prompt construct karna. Agar `selected_text` available ho, toh usse retrieved chunks se pehle rakhna:
            ```
            Use the following context from the book to answer the question:

            Context:
            {selected_text} // Agar available ho
            {retrieved_chunks_content}

            Question:
            {user_message}

            Provide a concise answer based on the provided context.
            ```
        -   `OpenAIService.generate_response()` call karke constructed prompt se `bot_response` lena.
        -   `conversation_id` (UUID) generate karna.
        -   `database.save_chat_history()` call karke `user_message`, `bot_response`, aur `selected_text` ko `conversation_id` ke saath store karna.
        -   JSON response return karna jismein `{"response": bot_response, "conversation_id": str(conversation_id)}` hoga.

## Acceptance Criteria

- [ ] `backend/` directory create ho gaya hai jismein `main.py`, `requirements.txt`, `database.py`, `qdrant_client.py`, aur `openai_service.py` hain.
- [ ] `requirements.txt` mein sabhi specified Python dependencies shamil hain.
- [ ] FastAPI application `uvicorn` ke saath successfully run hota hai.
- [ ] `/chat` endpoint POST requests ko accept karta hai jismein `user_message` aur optional `selected_text` hota hai.
- [ ] User messages ko OpenAI `text-embedding-3-small` use karke successfully embed kiya jata hai.
- [ ] Qdrant search correctly top 3 relevant book chunks retrieve karta hai.
- [ ] RAG prompt ko `user_message` aur, agar provide kiya gaya ho, toh `selected_text` (retrieved chunks se pehle) ke saath sahi tarah se construct kiya jata hai.
- [ ] OpenAI `gpt-4o-mini` ek coherent `bot_response` generate karta hai.
- [ ] Conversation history, jismein `selected_text` bhi shamil hai, Neon Postgres `chat_history` table mein accurately save hoti hai.
- [ ] `/chat` endpoint `response` aur `conversation_id` return karta hai.
- [ ] Invalid input, embedding failures, Qdrant search failures, LLM generation failures, aur database errors ke liye basic error handling implement kiya gaya hai.

## Follow-up Tasks / Risks

- Dockerfile add karne par विचार karein containerization aur easy deployment ke liye.
- Har component ke liye comprehensive unit aur integration tests implement karein.
- Behtar response quality aur hallucinations kam karne ke liye prompt engineering ko refine karein.
- User authentication aur authorization ko implement karne par विचार karein (bonus points).
- Content personalization aur translation features ko explore karein (bonus points).