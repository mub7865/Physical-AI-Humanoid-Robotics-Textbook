# Feature Tasks: Reusable Intelligence Layer (5 Critical Skills)

**Feature Branch**: `002-matrix-skills-v2`
**Date**: 2025-11-29
**Spec**: [./specs/002-matrix-skills-v2/spec.md](specs/002-matrix-skills-v2/spec.md)
**Plan**: [./specs/002-matrix-skills-v2/plan.md](specs/002-matrix-skills-v2/plan.md)

## Summary

This document outlines the detailed tasks required to implement the Reusable Intelligence Layer, focusing on the creation of 5 critical AI-native skills with their defined folder structure and initial Python logic. Tasks are organized by user story for independent development and testing.

## Phase 1: Setup

- [X] T001 Update `backend/requirements.txt` with `openai`, `tiktoken`, `python-dotenv`, `qdrant-client` `backend/requirements.txt`

## Phase 2: User Story 1 - Curriculum Design [US1]

**Goal**: As an author, I want to auto-generate the book structure from a syllabus file so that the hierarchy matches the course exactly.
**Independent Test**: Verify the creation of the specified directories and `.md` files in `book/docs/` after executing the `structure.py` script.

- [X] T002 [US1] Create directory `.claude/skills/curriculum-designer/`
- [X] T003 [US1] Create `SKILL.md` in `.claude/skills/curriculum-designer/SKILL.md`
- [X] T004 [US1] Create `scripts/` directory in `.claude/skills/curriculum-designer/scripts/`
- [X] T005 [US1] Write `structure.py` for Curriculum Designer in `.claude/skills/curriculum-designer/scripts/structure.py`

## Phase 3: User Story 2 - Pedagogical Enhancement [US2]

**Goal**: As a teacher, I want to simplify complex text using AI so that beginners can understand it easily.
**Independent Test**: Verify that the `teach.py` script takes text input and returns a simplified version with analogies and quiz questions using `openai.Client`.

- [X] T006 [P] [US2] Create directory `.claude/skills/pedagogue/`
- [X] T007 [P] [US2] Create `SKILL.md` in `.claude/skills/pedagogue/SKILL.md`
- [X] T008 [P] [US2] Create `scripts/` directory in `.claude/skills/pedagogue/scripts/`
- [X] T009 [P] [US2] Write `teach.py` for The Pedagogue in `.claude/skills/pedagogue/scripts/teach.py`

## Phase 4: User Story 3 - Agent Scaffolding [US3]

**Goal**: As a developer, I want to generate OpenAI Agent boilerplate code automatically to ensure I follow official patterns.
**Independent Test**: Verify that the `scaffold.py` script generates valid `worker.py` files in `backend/agents/` based on a template.

- [X] T010 [P] [US3] Create directory `.claude/skills/brain-builder/`
- [X] T011 [P] [US3] Create `SKILL.md` in `.claude/skills/brain-builder/SKILL.md`
- [X] T012 [P] [US3] Create `scripts/` directory in `.claude/skills/brain-builder/scripts/`
- [X] T013 [P] [US3] Write `scaffold.py` for Brain Builder in `.claude/skills/brain-builder/scripts/scaffold.py`

## Phase 5: User Story 4 - Knowledge Ingestion [US4]

**Goal**: As a librarian, I want to upload book content to Qdrant so the chatbot has knowledge.
**Independent Test**: Verify that the `ingest.py` script chunks text, generates OpenAI embeddings, and uploads vectors to Qdrant.

- [X] T014 [P] [US4] Create directory `.claude/skills/librarian/`
- [X] T015 [P] [US4] Create `SKILL.md` in `.claude/skills/librarian/SKILL.md`
- [X] T016 [P] [US4] Create `scripts/` directory in `.claude/skills/librarian/scripts/`
- [X] T017 [P] [US4] Write `ingest.py` for Librarian in `.claude/skills/librarian/scripts/ingest.py`

## Phase 6: User Story 5 - Deployment [US5]

**Goal**: As a publisher, I want to deploy the site to GitHub Pages with one command.
**Independent Test**: Verify that the `publish.py` script successfully builds the Docusaurus site and initiates the deployment process to GitHub Pages.

- [X] T018 [P] [US5] Create directory `.claude/skills/publisher/`
- [X] T019 [P] [US5] Create `SKILL.md` in `.claude/skills/publisher/SKILL.md`
- [X] T020 [P] [US5] Create `scripts/` directory in `.claude/skills/publisher/scripts/`
- [X] T021 [P] [US5] Write `publish.py` for Publisher in `.claude/skills/publisher/scripts/publish.py`

## Phase 7: Polish & Cross-Cutting Concerns

- [X] T022 Generate `sidebars.ts` (placeholder for `curriculum-designer` skill integration) in `book/sidebars.ts`

## Dependencies

- Phase 1 must be completed before any User Story phases.
- User Stories (Phase 2-6) can largely be developed in parallel due to their independent nature.

## Parallel Execution Examples

**Example 1 (Multiple Skill Directory Creation)**:
- `T002 [US1]` Create directory `.claude/skills/curriculum-designer/`
- `T006 [P] [US2]` Create directory `.claude/skills/pedagogue/`
- `T010 [P] [US3]` Create directory `.claude/skills/brain-builder/`

**Example 2 (Multiple Skill Script Writing)**:
- `T005 [US1]` Write `structure.py` for Curriculum Designer
- `T009 [P] [US2]` Write `teach.py` for The Pedagogue
- `T013 [P] [US3]` Write `scaffold.py` for Brain Builder

## Implementation Strategy

We will adopt an incremental delivery strategy, prioritizing the completion of each user story individually. Phase 1 (Setup) is a blocking prerequisite. User Stories (Phases 2-6) can be implemented and tested in parallel. The final polish phase will address cross-cutting concerns.
