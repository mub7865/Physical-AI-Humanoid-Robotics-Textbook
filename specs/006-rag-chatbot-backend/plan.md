Here is the detailed and updated implementation plan for the '006-rag-chatbot-backend' feature, explicitly incorporating the handling of `selected_text` in the RAG prompt.

## Implementation Plan for '006-rag-chatbot-backend'

This plan outlines the architecture and step-by-step implementation strategy for the RAG Chatbot Backend, with a particular focus on integrating `selected_text` into the RAG prompt.

### 1. Scope and Dependencies

**In Scope:**
- Development of a FastAPI server (`backend/main.py`) for the RAG chatbot.
- Implementation of the `POST /chat` endpoint to handle user queries.
- Integration with Neon Postgres for saving chat history.
- Integration with Qdrant for retrieving relevant book content.
- Usage of OpenAI `text-embedding-3-small` for embedding user messages.
- Usage of OpenAI `gpt-4o-mini` for generating chatbot answers.
- Saving conversation history (user message, bot response, and user selected text) in Neon Postgres.
- **Specifically:** Handling user-selected text as additional context with the `user_message`, placing it before the retrieved book chunks in the RAG prompt.

**Logic Flow Details for RAG Prompt Construction:**
- If `selected_text` is provided, it will be included in the prompt *before* the retrieved book chunks.
- The prompt structure will be as follows:
  ```
  Use the following context from the book to answer the question:

  Context:
  {selected_text} // If available
  {retrieved_chunks_content}

  Question:
  {user_message}

  Provide a concise answer based on the provided context.
  ```

**Out of Scope:**
- Frontend development for the RAG chatbot.
- User authentication and authorization (for the initial version).
- Advanced chat features (e.g., streaming responses, multi-turn conversations).
- Enhanced error handling beyond basic API responses.
- Deployment infrastructure setup (e.g., Dockerization, CI/CD).

**External Dependencies:**
- **FastAPI:** Python web framework for building the API.
- **Neon Postgres:** Database for chat history.
  - Client: `psycopg2-binary`.
- **Qdrant:** Vector database for book knowledge.
  - Client: `qdrant-client`.
- **OpenAI:** For embeddings and language model generation.
  - Models: `text-embedding-3-small` (for embeddings), `gpt-4o-mini` (for generation).
  - SDK: `openai` Python client.

### 2. Key Decisions and Rationale

**Options Considered:**
- **Chat History Database:** PostgreSQL (Neon) vs. SQLite vs. MongoDB.
  - **Trade-offs:** PostgreSQL is robust and scalable. SQLite is simple but not suitable for production. MongoDB offers flexibility but is overkill for simple chat history.
  - **Rationale:** Neon Postgres was selected due to its cloud-native capabilities and production-grade requirements. `psycopg2-binary` is a standard PostgreSQL adapter for Python.
- **Vector Database:** Qdrant vs. Pinecone vs. FAISS.
  - **Trade-offs:** Qdrant offers self-hosting flexibility and good performance. Pinecone is a managed service. FAISS is a local library.
  - **Rationale:** Qdrant is specified in the project context, providing a scalable and efficient solution for vector search.
- **LLM for Generation:** `gpt-4o-mini` vs. `gpt-4o`.
  - **Trade-offs:** `gpt-4o-mini` provides a good balance of cost-effectiveness and performance. `gpt-4o` offers higher quality but is more expensive.
  - **Rationale:** `gpt-4o-mini` was chosen to optimize cost and latency while delivering good responses for the RAG use case.

### 3. Interfaces and API Contracts

**Public APIs:**

#### POST `/chat`
- **Description:** Takes a user message, processes it using RAG, generates a response, and saves the conversation history. If provided, user-selected text will be included as additional context, placed before retrieved chunks.
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "user_message": "string",
    "selected_text": "string" // Optional: Text selected by the user from the book
  }
  ```
- **Response Body (Success 200 OK):**
  ```json
  {
    "response": "string",
    "conversation_id": "string"
  }
  ```
- **Error Taxonomy:**
  - **400 Bad Request:**
    - `{"detail": "Invalid input: user_message is required."}`
    - `{"detail": "Embedding failed."}`
    - `{"detail": "Qdrant search failed."}`
    - `{"detail": "LLM generation failed."}`
  - **500 Internal Server Error:**
    - `{"detail": "Database error: Failed to save chat history."}`
    - `{"detail": "An unexpected error occurred."}`

**Versioning Strategy:**
- Initial versioning will be implicit. API versioning (e.g., `/v1/chat`) will be considered for future iterations.

**Idempotency, Timeouts, Retries:**
- **Idempotency:** Not strictly necessary for the `/chat` endpoint, as saving history maintains state.
- **Timeouts:** Will be managed at the API gateway or application server level.
- **Retries:** Retries with exponential backoff will be implemented for external services (OpenAI, Qdrant, Neon Postgres).

### 4. Non-Functional Requirements (NFRs) and Budgets

**Performance:**
- **p95 latency for `/chat`:** < 2 seconds (target).
- **Throughput:** Capacity to handle 50 requests per second with current infrastructure.
- **Resource Caps:** CPU, memory, and network usage will be monitored and optimized.

**Reliability:**
- **SLO:** 99.9% availability for the `/chat` endpoint.
- **Error Budgets:** < 0.1% requests with 5xx errors.
- **Degradation Strategy:** In case of external service (OpenAI, Qdrant) failures, the system will gracefully return an error message to the user.

**Security:**
- **AuthN/AuthZ:** No authentication/authorization for the initial version. To be added in future iterations.
- **Data Handling:** User messages, AI responses, and selected text stored in Neon Postgres will be considered sensitive data.
- **Secrets:** API keys for OpenAI, Neon Postgres, and Qdrant will be securely managed using environment variables.
- **Auditing:** Basic logging for requests and responses for debugging and monitoring.

**Cost:**
- **Unit Economics:** Minimize OpenAI API calls (using `gpt-4o-mini` and efficient token usage) and Qdrant/Neon hosting costs.

### 5. Data Management and Migration

**Source of Truth:**
- **Chat History:** Neon Postgres `chat_history` table.
- **Book Knowledge:** Qdrant `book_knowledge` collection.

**Schema Evolution:**
- The `chat_history` table schema will be designed flexibly for future additions (e.g., message metadata, user IDs). Schema migrations will be handled using appropriate database migration tools (if the project scales).

**Chat History Table Schema (Neon Postgres):**
The `chat_history` table will have the following columns:
- `conversation_id` (UUID, Primary Key)
- `user_message` (TEXT, NOT NULL)
- `bot_response` (TEXT, NOT NULL)
- `selected_text` (TEXT, NULLABLE) - New column for user-selected text.
- `timestamp` (TIMESTAMP WITH TIME ZONE, NOT NULL, DEFAULT NOW())

**Migration and Rollback:**
- Initial data (book content in Qdrant) will be pre-loaded. Chat history data will be generated from user interaction.
- Rollback strategies for database schema changes will be considered.

**Data Retention:**
- Chat history will be retained indefinitely in Neon Postgres until specific retention policies are defined.

### 6. Operational Readiness

**Observability:**
- **Logs:** Structured logging (e.g., JSON format) for application events, errors, and performance metrics.
- **Metrics:** Prometheus/Grafana (or similar) integration for API latency, error rates, and resource utilization monitoring.
- **Traces:** Distributed tracing (e.g., OpenTelemetry) for tracking services across requests (future consideration).

**Alerting:**
- **Thresholds:** Alerts for high error rates, increased latency, or critical service outages.
- **On-call Owners:** To be defined if the project goes into production.

**Runbooks for common tasks:**
- Basic runbooks for deploying the backend, restarting services, and checking logs.

**Deployment and Rollback strategies:**
- **Deployment:** Standard CI/CD pipeline for deploying the FastAPI application (if implemented).
- **Rollback:** Ability to revert to the previous stable version in case of critical issues.

**Feature Flags and compatibility:**
- Not applicable for the initial version.

### 7. Risk Analysis and Mitigation

**Top 3 Risks:**
1.  **OpenAI API Rate Limits:**
    -   **Blast Radius:** Service degradation or unavailability upon hitting rate limits.
    -   **Mitigation:** Implement rate limit handling with retries and exponential backoff. Monitor usage and scale up API quotas if necessary.
2.  **Qdrant/Neon Postgres Downtime:**
    -   **Blast Radius:** Inability to retrieve knowledge or save chat history.
    -   **Mitigation:** Implement robust error handling and retries. Consider caching strategies for Qdrant (read-heavy). Ensure database backups and replication.\n3.  **LLM Hallucinations/Poor Quality Responses:**\n    -   **Blast Radius:** Providing incorrect or unhelpful information to users.\n    -   **Mitigation:** Fine-tune RAG prompt engineering. Implement user feedback mechanisms. Regularly evaluate the quality of LLM responses.\n\n### 8. Evaluation and Validation\n\n**Definition of Done:**\n- All specified API endpoints are implemented and functional.\n- Integration with Neon Postgres and Qdrant is successful.\n- End-to-end RAG logic (embedding, search, prompt construction, generation) is working correctly.\n- If provided, user-selected text is correctly incorporated into the RAG prompt *before* the retrieved chunks.\n- Unit and integration tests cover critical paths.\n- Code adheres to project standards and constraints.\n\n**Output Validation for format/requirements/safety:**\n- API responses conform to the defined JSON schema.\n- LLM-generated content is reviewed for safety and relevance.\n\n### 9. Architectural Decision Record (ADR) - Intelligent Suggestion\n📋 Architectural decision detected: RAG Chatbot Backend with Selected Text Integration. Document reasoning and tradeoffs? Run `/sp.adr RAG-Chatbot-Backend-Selected-Text-Integration`\n\n---\n\n### Python Dependencies (`requirements.txt`):\n\n```\nfastapi\nuvicorn\nopenai\nqdrant-client\npsycopg2-binary\npython-dotenv\n```\n\n### Critical Files for Implementation\n- `/mnt/d/AI-DRIVEN_AND_SPEC-DRIVEN_HACKATHON/backend/main.py` - Core FastAPI application and `/chat` endpoint logic, including `selected_text` handling in prompt construction.\n- `/mnt/d/AI-DRIVEN_AND_SPEC-DRIVEN_HACKATHON/backend/database.py` - Database connection and chat history management with Neon Postgres, specifically handling the `selected_text` column.\n- `/mnt/d/AI-DRIVEN_AND_SPEC-DRIVEN_HACKATHON/backend/qdrant_client.py` - Qdrant client initialization and search logic to retrieve relevant chunks.\n- `/mnt/d/AI-DRIVEN_AND_SPEC-DRIVEN_HACKATHON/backend/openai_service.py` - OpenAI embedding and LLM generation service, responsible for constructing the RAG prompt with `selected_text` before retrieved chunks.\n- `/mnt/d/AI-DRIVEN_AND_SPEC-DRIVEN_HACKATHON/specs/006-rag-chatbot-backend/plan.md` - This detailed plan document.