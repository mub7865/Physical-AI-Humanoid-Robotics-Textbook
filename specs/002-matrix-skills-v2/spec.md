# Feature Specification: Reusable Intelligence Layer (5 Critical Skills)

**Feature Branch**: `002-matrix-skills-v2`
**Status**: Approved

## User Scenarios

### User Story 1 - Curriculum Design
As an author, I want to auto-generate the book structure from a syllabus file so that the hierarchy matches the course exactly.
**Acceptance**: `curriculum-designer` skill reads `specs/input/syllabus.md` and creates empty `.md` files in `book/docs/`.

### User Story 2 - Pedagogical Enhancement
As a teacher, I want to simplify complex text using AI so that beginners can understand it easily.
**Acceptance**: `pedagogue` skill takes text input and returns a simplified version with analogies and quiz questions.

### User Story 3 - Agent Scaffolding
As a developer, I want to generate OpenAI Agent boilerplate code automatically to ensure I follow official patterns.
**Acceptance**: `brain-builder` skill generates valid `worker.py` files in `backend/agents/`.

### User Story 4 - Knowledge Ingestion
As a librarian, I want to upload book content to Qdrant so the chatbot has knowledge.
**Acceptance**: `librarian` skill chunks text and uploads vectors to Qdrant.

### User Story 5 - Deployment
As a publisher, I want to deploy the site to GitHub Pages with one command.
**Acceptance**: `publisher` skill builds and deploys the site.

## Requirements (The Folder Structure)

- **FR-001**: Create `.claude/skills/curriculum-designer/` with `SKILL.md` and `scripts/structure.py`.
- **FR-002**: Create `.claude/skills/pedagogue/` with `SKILL.md` and `scripts/teach.py` (Logic: LLM-based simplification).
- **FR-003**: Create `.claude/skills/brain-builder/` with `SKILL.md` and `scripts/scaffold.py` (Logic: OpenAI SDK templates).
- **FR-004**: Create `.claude/skills/librarian/` with `SKILL.md` and `scripts/ingest.py` (Logic: Qdrant upload).
- **FR-005**: Create `.claude/skills/publisher/` with `SKILL.md` and `scripts/publish.py` (Logic: Git deploy).

## Success Criteria
- **SC-001**: All 5 folders exist in `.claude/skills/`.
- **SC-002**: Each skill has a Python script executable via CLI.