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
**Goal:** Build an "AI-Native Interactive Book" using Docusaurus (Frontend) and FastAPI (Backend) with an embedded RAG Chatbot.
**Core Feature:** Users must be able to select text on the book to ask context-aware questions.
**Governance:**
- **Supreme Law:** This file overrides all other defaults.
- **ZERO VIBE CODING:** Development is FORBIDDEN without an existing `spec.md` and `plan.md`.
- **Workflow:** `sp.specify` (Define) -> `sp.plan` (Architect) -> `sp.implement` (Code).

## 2. Mandatory Tech Stack (Non-Negotiable)
- **Frontend:** Docusaurus 3.9 (Classic Theme), React.
- **Backend:** Python 3.10+, FastAPI, Uvicorn.
- **AI Brain:** OpenAI Agents SDK (Reasoning) + Gemini Flash (Code Gen via Router).
- **Vector Database:** Qdrant Cloud (Free Tier).
- **Embeddings:** OpenAI `text-embedding-3-small` (Cost-efficient).

## 3. The "Matrix" Protocol (Reusable Intelligence)
**Rule:** We build **"Agent Skills"**, not scripts.
- **Librarian Skill (`skills/ingest.py`):**
    - MUST read all `.md` files from `book/docs/`.
    - MUST use `RecursiveCharacterTextSplitter` (chunk size ~1000).
    - MUST upload vectors to Qdrant collection `book_knowledge`.
- **Publisher Skill (`skills/publish.py`):**
    - MUST build the Docusaurus site (`npm run build`).
    - MUST deploy to GitHub Pages (`npm run deploy`).

## 4. RAG & Frontend-Backend Contract
**The "Select Text" Feature Logic:**
1.  **Frontend:** The Chat Widget must be injected into the Docusaurus `Layout` (using Swizzling or Wrapper) so it appears on *every* page.
2.  **Event Listener:** The Widget must listen for `mouseup` events to capture selected text.
3.  **API Payload:**
    ```json
    POST /chat
    {}
      "message": "User question",
      "context": "The text user selected (if any)"
    }
    ```
4.  **Backend Logic:** If `context` is provided, the Agent answers based on that. If not, it searches Qdrant (RAG).

## 5. Directory Structure Map (Strict Enforcement)
- `specs/` (Specs, Plans, Tasks)
- `book/` (Docusaurus Frontend Source)
- `backend/` (FastAPI Source & Virtual Env)
- `skills/` (Reusable Agent Scripts)
- `.specify/` (SpecKit Templates)
- `.claude/` (Command definitions)

## 6. Development Guidelines
- **Testing:** Verify the Chatbot works with AND without selected text.
- **Deployment:** Ensure `docusaurus.config.js` is configured for GitHub Pages (baseUrl/url).
- **ADR:** Document any schema changes in Qdrant via `sp.adr`.

## 7. Content Standards & Quality
- **Writing Clarity:** Book content MUST achieve a Flesch-Kincaid Grade Level of 10-12, with at least 75% of sentences in active voice (automatable check).
- **Source Verification & Citation Accuracy:** All factual claims in the book content MUST be supported by external references, cited using a consistent format (e.g., Markdown footnotes or bibliography). References MUST be verifiable through a specified process (e.g., automated link checker for online sources, or manual review for academic papers).
- **Content Review Process:** New or significantly updated book chapters MUST undergo a peer review process before merging, requiring at least one approval from a designated content reviewer.

**Version**: 0.0.7 (Comprehensive) | **Ratified**: 2025-11-28
