<!--
Sync Impact Report:
Version change: 0.0.6 (old) → 0.0.7 (new)
List of modified principles:
- Added Content Standards & Quality section (new).
Added sections: 7. Content Standards & Quality
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md: ⚠ pending
- .specify/templates/spec-template.md: ⚠ pending
- .specify/templates/tasks-template.md: ⚠ pending
- .claude/commands/sp.adr.md: ⚠ pending
- .claude/commands/sp.analyze.md: ⚠ pending
- .claude/commands/sp.checklist.md: ⚠ pending
- .claude/commands/sp.clarify.md: ⚠ pending
- .claude/commands/sp.constitution.md: ⚠ pending
- .claude/commands/sp.git.commit_pr.md: ⚠ pending
- .claude/commands/sp.implement.md: ⚠ pending
- .claude/commands/sp.phr.md: ⚠ pending
- .claude/commands/sp.plan.md: ⚠ pending
- .claude/commands/sp.specify.md: ⚠ pending
- .claude/commands/sp.tasks.md: ⚠ pending
- README.md: ⚠ pending
Follow-up TODOs: None
-->
# AI-Native Interactive Book Constitution

## 1. Project Vision & Governance
**Goal:** Build an "AI-Native Interactive Book" hosted on GitHub Pages with an embedded RAG Chatbot.
**Official Mandate:** Strictly follow the Panaversity Hackathon I guidelines (Google Doc).
**Governance:**
- **ZERO VIBE CODING:** Development is FORBIDDEN without an existing `spec.md` and `plan.md`.
- **Workflow:** `sp.specify` (Define) -> `sp.plan` (Architect) -> `sp.implement` (Code).

## 2. Mandatory Tech Stack (The "Official" Stack)
- **Frontend:** Docusaurus 3.9 (Classic), React, Tailwind CSS.
- **Backend:** Python 3.10+, FastAPI, Uvicorn.
- **AI Brain:** OpenAI Agents SDK (Logic) + Gemini Flash (via Router for Code Gen).
- **Vector Database:** **Qdrant Cloud** (For RAG/Embeddings).
- **Relational Database:** **Neon Serverless Postgres** (For Chat History & User Data).
- **Deployment:** GitHub Pages (Frontend) & Vercel/Render (Backend).

## 3. Feature Roadmap (Prioritized)
**Phase 1: The Core (Must Complete First)**
- RAG Chatbot answering from the book using Qdrant.
- "Select Text" feature (Context-Aware API).
- Reusable Skills (`skills/librarian.py`, `skills/publisher.py`).

**Phase 2: The Bonus (Target: 50 Marks)**
- **Authentication:** Implement `Better-Auth` for User Signup/Login.
- **Personalization:** Store user preferences in Neon Postgres.

## 4. The "Matrix" Protocol (Reusable Intelligence)
**Rule:** We build **"Agent Skills"** located in `skills/`.
- **Librarian Skill (`skills/ingest.py`):**
    - MUST read `.md` files -> Chunk -> Embed (OpenAI Small) -> Upload to Qdrant.
- **Publisher Skill (`skills/publish.py`):**
    - MUST build Docusaurus -> Deploy to GitHub Pages.

## 5. RAG & API Contract
**The "Select Text" Logic:**
1.  **Frontend:** Widget listens for `mouseup` events on Docusaurus pages.
2.  **API Payload:**
    ```json
    POST /chat
    {
      "message": "User question",
      "context": "Selected text (optional)",
      "user_id": "From Better-Auth (optional)"
    }
    ```
3.  **Backend Logic:**
    - Save chat history to **Neon Postgres**.
    - If `context` exists, answer from context. Else, search **Qdrant**.

## 6. Content Standards
- **Writing Quality:** Book content must be Flesch-Kincaid Grade 10-12 (Professional & Clear).
- **Source:** Content must be AI-generated based on the provided Topic.

**Version**: 1.0.0 (Official Compliant) | **Ratified**: 2025-11-29