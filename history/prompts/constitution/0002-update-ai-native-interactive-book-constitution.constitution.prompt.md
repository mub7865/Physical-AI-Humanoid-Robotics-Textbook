---
id: 0002
title: Update AI-Native Interactive Book Constitution
stage: constitution
date: 2025-11-28
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: User
command: /sp.constitution Act as a Chief AI Architect for a high-stakes Hackathon project. I need you to generate a strict Project Constitution. You must overwrite any existing constitution with these specific rules derived from the Hackathon requirements. Here are the Rules for the Constitution: 1. **Project Vision:** - Build an "AI-Native Interactive Book" using Docusaurus (Frontend) and FastAPI (Backend). - The system MUST include a RAG Chatbot powered by OpenAI Agents SDK and Qdrant Vector DB. - Users must be able to select text on the book to ask context-aware questions. 2. **Mandatory Tech Stack (No Deviations):** - Frontend: Docusaurus 3.9 (Classic Template), React for Chat Widget. - Backend: Python 3.10+, FastAPI, Uvicorn. - AI/Logic: OpenAI Agents SDK (or ChatKit), Gemini 1.5 Flash (via Router) for generation. - Database: Qdrant Cloud (Free Tier) for Vector Storage. 3. **Spec-Driven Development (SDD) Mandate:** - **ZERO VIBE CODING POLICY:** You are FORBIDDEN from writing implementation code without an existing `spec.md` and `plan.md` in the `specs/` folder. - Workflow: Always ask "Have we specified this?" -> Run `sp.specify` -> Run `sp.plan` -> Run `sp.implement`. 4. **The "Matrix" Protocol (Bonus Marks Strategy):** - Prioritize "Reusable Intelligence" over hardcoded logic. - Whenever a repetitive task is identified (e.g., Ingesting books to DB, Deploying to GitHub), you must create a reusable Python script in the `skills/` folder (e.g., `skills/librarian.py`, `skills/publisher.py`). - These skills should be treated as "Agent Skills" that can be invoked via CLI. 5. **Deployment Standards:** - The book must be deployable to GitHub Pages. - Code must be modular and clean. Please generate the full content of `.specify/memory/constitution.md` now.
labels: ["governance", "constitution", "hackathon"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
- .specify/memory/constitution.md
tests:

---

## Prompt

Act as a Chief AI Architect for a high-stakes Hackathon project.
I need you to generate a strict Project Constitution.

You must overwrite any existing constitution with these specific rules derived from the Hackathon requirements.

Here are the Rules for the Constitution:

1. **Project Vision:**
   - Build an "AI-Native Interactive Book" using Docusaurus (Frontend) and FastAPI (Backend).
   - The system MUST include a RAG Chatbot powered by OpenAI Agents SDK and Qdrant Vector DB.
   - Users must be able to select text on the book to ask context-aware questions.

2. **Mandatory Tech Stack (No Deviations):**
   - Frontend: Docusaurus 3.9 (Classic Template), React for Chat Widget.
   - Backend: Python 3.10+, FastAPI, Uvicorn.
   - AI/Logic: OpenAI Agents SDK (or ChatKit), Gemini 1.5 Flash (via Router) for generation.
   - Database: Qdrant Cloud (Free Tier) for Vector Storage.

3. **Spec-Driven Development (SDD) Mandate:**
   - **ZERO VIBE CODING POLICY:** You are FORBIDDEN from writing implementation code without an existing `spec.md` and `plan.md` in the `specs/` folder.
   - Workflow: Always ask "Have we specified this?" -> Run `sp.specify` -> Run `sp.plan` -> Run `sp.implement`.

4. **The "Matrix" Protocol (Bonus Marks Strategy):**
   - Prioritize "Reusable Intelligence" over hardcoded logic.
   - Whenever a repetitive task is identified (e.g., Ingesting books to DB, Deploying to GitHub), you must create a reusable Python script in the `skills/` folder (e.g., `skills/librarian.py`, `skills/publisher.py`).
   - These skills should be treated as "Agent Skills" that can be invoked via CLI.

5. **Deployment Standards:**
   - The book must be deployable to GitHub Pages.
   - Code must be modular and clean.

Please generate the full content of `.specify/memory/constitution.md` now.

## Response snapshot

The project constitution for the "AI-Native Interactive Book" has been updated to version 0.0.2. The constitution now includes core principles for Project Vision, Mandatory Tech Stack, Spec-Driven Development, The "Matrix" Protocol (Reusable Intelligence), and Deployment Standards. The governance section has also been updated. The ratification date remains a TODO.

## Outcome

- ✅ Impact: Constitution updated with new rules.
- 🧪 Tests: N/A
- 📁 Files: Modified .specify/memory/constitution.md
- 🔁 Next prompts: User approval of constitution.
- 🧠 Reflection: Successfully updated the project constitution based on user-provided rules.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
