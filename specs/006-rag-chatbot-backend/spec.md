# Feature Specification: RAG Chatbot Backend

## 1. Scope aur Dependencies

### In Scope:
- FastAPI server (`backend/main.py`) banana RAG chatbot ke liye.
- `POST /chat` endpoint implement karna user queries handle karne ke liye.
- Neon Postgres ke saath integration chat history save karne ke liye.
- Qdrant ke saath integration relevant book content retrieve karne ke liye.
- OpenAI `text-embedding-3-small` use karke user message ko embed karna.
- OpenAI `gpt-4o-mini` use karke chatbot answer generate karna.
- Conversation history (user message, bot response, aur user selected text) ko Neon Postgres mein save karna.
- **Khaas Taur Par:** User dwara select kiye gaye text ko `user_message` ke saath additional context ke taur par handle karna.

### Logic Flow Details for RAG Prompt Construction:
- Agar `selected_text` provide kiya gaya hai, toh yeh prompt mein retrieved book chunks se pehle shamil kiya jaega.
- Prompt ka structure kuch aisa hoga:
  ```
  Use the following context from the book to answer the question:

  Context:
  {selected_text} // Agar available ho
  {retrieved_chunks_content}

  Question:
  {user_message}

  Provide a concise answer based on the provided context.
  ```


### Out of Scope:
- RAG chatbot ke liye frontend development.
- User authentication aur authorization (initial version ke liye).
- Advanced chat features (jaise streaming responses, multi-turn conversations).
- Basic API responses ke ilawa behtar error handling.
- Deployment infrastructure setup (jaise Dockerization, CI/CD).

### External Dependencies:
- **FastAPI:** Python web framework API banane ke liye.
- **Neon Postgres:** Chat history ke liye database.
  - Client: `psycopg2-binary`.
- **Qdrant:** Book knowledge ke liye vector database.
  - Client: `qdrant-client`.
- **OpenAI:** Embeddings aur language model generation ke liye.
  - Models: `text-embedding-3-small` (embeddings ke liye), `gpt-4o-mini` (generation ke liye).
  - SDK: `openai` Python client.

## 2. Key Decisions aur Rationale

### Options Consider Kiye Gaye:
- **Chat History ke liye Database:** PostgreSQL (Neon) vs. SQLite vs. MongoDB.
  - **Trade-offs:** PostgreSQL robust aur scalable hai. SQLite simple hai lekin production ke liye sahi nahi. MongoDB flexible hai lekin simple chat history ke liye zyada hai.
  - **Rationale:** Neon Postgres ko cloud-native capabilities aur production-grade requirements ki wajah se chuna gaya hai. `psycopg2-binary` Python ke liye ek standard PostgreSQL adapter hai.
- **Vector Database:** Qdrant vs. Pinecone vs. FAISS.
  - **Trade-offs:** Qdrant self-hosting flexibility aur achhi performance deta hai. Pinecone managed service hai. FAISS local library hai.
  - **Rationale:** Qdrant ko project context mein specify kiya gaya hai, jo vector search ke liye scalable aur efficient solution provide karta hai.
- **LLM for Generation:** `gpt-4o-mini` vs. `gpt-4o`.
  - **Trade-offs:** `gpt-4o-mini` cost-effective aur performance ka achha balance hai. `gpt-4o` zyada quality deta hai lekin zyada costly hai.
  - **Rationale:** `gpt-4o-mini` ko cost aur latency optimize karne ke liye chuna gaya hai, RAG use case ke liye achhe responses deta hai.

## 3. Interfaces aur API Contracts

### Public APIs:

#### POST `/chat`
- **Description:** User message leta hai, RAG use karke process karta hai, response generate karta hai, aur conversation history save karta hai. Agar provide kiya gaya ho, toh user dwara selected text ko retrieved chunks se pehle rakhte hue, additional context ke taur par shamil kiya jaega.
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "user_message": "string",
    "selected_text": "string" // Optional: User dwara book se select kiya gaya text
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

### Versioning Strategy:
- Initial versioning implicit rahegi. API versioning (jaise `/v1/chat`) future iterations ke liye consider ki jaegi.

### Idempotency, Timeouts, Retries:
- **Idempotency:** `/chat` endpoint ke liye zaroori nahi. History save karna state maintain karta hai.
- **Timeouts:** API gateway ya application server level par manage kiye jaenge.
- **Retries:** External services (OpenAI, Qdrant, Neon Postgres) ke liye exponential backoff ke saath retries implement kiye jaenge.

## 4. Non-Functional Requirements (NFRs) aur Budgets

### Performance:
- **p95 latency for `/chat`:** < 2 seconds (target).
- **Throughput:** Current infrastructure ke saath 50 requests per second handle karne ki capacity.
- **Resource Caps:** CPU, memory, aur network usage ko monitor aur optimize kiya jaega.

### Reliability:
- **SLO:** `/chat` endpoint ke liye 99.9% availability.
- **Error Budgets:** < 0.1% requests mein 5xx errors.
- **Degradation Strategy:** External service (OpenAI, Qdrant) failures ke case mein, system user ko gracefully error message return karega.

### Security:
- **AuthN/AuthZ:** Initial version ke liye koi authentication/authorization nahi. Future iterations mein add kiya jaega.
- **Data Handling:** Neon Postgres mein store kiye gaye user messages, AI responses, aur selected text ko sensitive data mana jaega.
- **Secrets:** OpenAI, Neon Postgres, aur Qdrant ke API keys environment variables use karke securely manage kiye jaenge.
- **Auditing:** Basic logging requests aur responses ke liye debugging aur monitoring ke liye.

### Cost:
- **Unit Economics:** OpenAI API calls (using `gpt-4o-mini` aur efficient token usage) aur Qdrant/Neon hosting ke costs ko minimize karna.

## 5. Data Management aur Migration

### Source of Truth:
- **Chat History:** Neon Postgres `chat_history` table.
- **Book Knowledge:** Qdrant `book_knowledge` collection.

### Schema Evolution:
- `chat_history` table schema future additions (jaise message metadata, user IDs) ke liye flexible design kiya jaega. Schema migrations ko appropriate database migration tools (agar project bada hota hai) use karke handle kiya jaega.

### Chat History Table Schema (Neon Postgres):
`chat_history` table mein yeh columns honge (previous clarification ke mutabiq):
- `conversation_id` (UUID, Primary Key)
- `user_message` (TEXT, NOT NULL)
- `bot_response` (TEXT, NOT NULL)
- `selected_text` (TEXT, NULLABLE) - Naya column user selected text ke liye.
- `timestamp` (TIMESTAMP WITH TIME ZONE, NOT NULL, DEFAULT NOW())

### Migration aur Rollback:
- Initial data (book content in Qdrant) pre-loaded hoga. Chat history data user interaction se generate hoga.
- Database schema changes ke liye rollback strategies consider ki jaengi.

### Data Retention:
- Chat history Neon Postgres mein indefinitely retain kiya jaega jab tak koi specific retention policies define nahi ki jaati.

## 6. Operational Readiness

### Observability:
- **Logs:** Structured logging (jaise JSON format) application events, errors, aur performance metrics ke liye.
- **Metrics:** Prometheus/Grafana (ya similar) integration API latency, error rates, aur resource utilization monitoring ke liye.
- **Traces:** Distributed tracing (jaise OpenTelemetry) services across requests track karne ke liye (future consideration).

### Alerting:
- **Thresholds:** High error rates, increased latency, ya critical service outages ke liye alerts.
- **On-call Owners:** Agar project production mein jaata hai toh define kiye jaenge.

### Runbooks for common tasks:
- Backend deploy karne, services restart karne, aur logs check karne ke liye basic runbooks.

### Deployment aur Rollback strategies:
- **Deployment:** FastAPI application deploy karne ke liye standard CI/CD pipeline (agar implement hota hai).
- **Rollback:** Critical issues ke case mein pichhle stable version par revert karne ki ability.

### Feature Flags aur compatibility:
- Initial version ke liye applicable nahi.

## 7. Risk Analysis aur Mitigation

### Top 3 Risks:
1.  **OpenAI API Rate Limits:**
    -   **Blast Radius:** Rate limits hit hone par service degradation ya unavailability.
    -   **Mitigation:** Retries aur exponential backoff ke saath rate limit handling implement karna. Usage monitor karna aur API quotas scale up karna agar zaroori ho.
2.  **Qdrant/Neon Postgres Downtime:**
    -   **Blast Radius:** Knowledge retrieve karne ya chat history save karne mein asamarthata.
    -   **Mitigation:** Robust error handling aur retries implement karna. Qdrant ke liye caching strategies consider karna (read-heavy). Database backups aur replication ensure karna.
3.  **LLM Hallucinations/Poor Quality Responses:**
    -   **Blast Radius:** Users ko galat ya bekar information provide karna.
    -   **Mitigation:** RAG prompt engineering ko fine-tune karna. User feedback mechanisms implement karna. LLM responses ki quality regularly evaluate karna.

## 8. Evaluation aur Validation

### Definition of Done:
- Sabhi specified API endpoints implemented aur functional hain.
- Neon Postgres aur Qdrant ke saath integration successful hai.
- End-to-end RAG logic (embedding, search, prompt construction, generation) theek se kaam kar rahi hai.
- Agar provide kiya gaya ho, toh user selected text ko RAG prompt mein retrieved chunks se pehle rakhte hue sahi tarah se incorporate kiya ja raha hai.
- Unit aur integration tests critical paths ko cover karte hain.
- Code project standards aur constraints ko follow karta hai.

### Output Validation for format/requirements/safety:
- API responses defined JSON schema ke mutabiq hain.
- LLM generated content safety aur relevance ke liye review kiya gaya hai.

## 9. Architectural Decision Record (ADR):
📋 Architectural decision detected: RAG Chatbot Backend with Selected Text Integration. Document reasoning and tradeoffs? Run `/sp.adr RAG-Chatbot-Backend-Selected-Text-Integration`

---

### Python Dependencies (`requirements.txt`):

```
fastapi
uvicorn
openai
qdrant-client
psycopg2-binary
python-dotenv
```

### Critical Files for Implementation
- `/mnt/d/AI-DRIVEN_AND_SPEC-DRIVEN_HACKATHON/backend/main.py` - Core FastAPI application aur `/chat` endpoint logic.
- `/mnt/d/AI-DRIVEN_AND_SPEC-DRIVEN_HACKATHON/backend/database.py` - Database connection aur chat history management with Neon Postgres.
- `/mnt/d/AI-DRIVEN_AND_SPEC-DRIVEN_HACKATHON/backend/qdrant_client.py` - Qdrant client initialization aur search logic.
- `/mnt/d/AI-DRIVEN_AND_SPEC-DRIVEN_HACKATHON/backend/openai_service.py` - OpenAI embedding aur LLM generation service.
- `/mnt/d/AI-DRIVEN_AND_SPEC-DRIVEN_HACKATHON/specs/006-rag-chatbot-backend/plan.md` - Yeh detailed plan document (ab update kiya jaega).
