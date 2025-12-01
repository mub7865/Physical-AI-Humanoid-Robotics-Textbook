# Feature Specification: Project Skeleton & Tooling

**Feature Branch**: `001-project-init`
**Created**: 2025-11-29
**Status**: Draft
**Input**: User description: "Act as a Senior AI Architect following the Spec-Kit Plus protocol.
I want to initiate the "Specify Phase" for our first feature.

**Command:** Run `sp.specify` logic.

**Feature Name:** `01-project-init` (Project Skeleton & Tooling)

**Context:**
We need to set up the foundational structure for the "AI-Native Interactive Book" hackathon project.
The goal is to create the directory structure and install base dependencies without writing business logic yet.

**Requirements to Cover:**
1. Root directory structure (`book/`, `backend/`, `skills/`, `specs/`).
2. Docusaurus 3.9 (Classic) installation in `book/`.
3. Python FastAPI + Uvicorn + Qdrant Client setup in `backend/`.
4. Creation of placeholder Skill files (`ingest.py`, `publish.py`) in `skills/`.
5. Configuration of `CLAUDE.md` and `.specify/` templates if missing.

**YOUR INSTRUCTION:**
Do NOT generate the spec file immediately. That would be "Vibe Coding".
Instead, ask me 3-5 critical clarifying questions to ensure you understand the technology versions, naming conventions, and environment constraints.
Once I answer, ONLY THEN generate the file at `specs/01-project-init/spec.md`."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Project Initialization (Priority: P1)

A developer wants to quickly set up the foundational project structure and essential tooling to begin development on the AI-Native Interactive Book.

**Why this priority**: This is the absolute first step for any developer to get the project running and is critical for team onboarding and initial development.

**Independent Test**: Can be fully tested by cloning the repository, running the setup script/commands, and verifying that all specified directories exist and core dependencies are installed/configured, allowing for basic local development and building.

**Acceptance Scenarios**:

1. **Given** a fresh development environment, **When** the project initialization steps are executed, **Then** the `book/`, `backend/`, `skills/`, and `specs/` root directories are created.
2. **Given** the `book/` directory is created, **When** Docusaurus 3.9 (Classic) is installed, **Then** a functional Docusaurus site structure is present and can be built.
3. **Given** the `backend/` directory is created, **When** Python 3.12, FastAPI, Uvicorn, and Qdrant Client are set up, **Then** a `main.py` with a basic "Hello World" endpoint is available and the backend service can be started.
4. **Given** the `skills/` directory is created, **When** placeholder `ingest.py` and `publish.py` files are created, **Then** these files exist and are accessible.
5. **Given** the project's root directory, **When** `CLAUDE.md` and essential `.specify/` templates are checked, **Then** missing templates are configured to their default states.

---

### Edge Cases

- What happens if a required directory already exists during initialization? (Should gracefully skip creation)
- How does the system handle failed dependency installations? (Should report errors clearly and stop if critical)
- What if a Docusaurus or Python dependency conflicts with existing system-wide packages? (Should ideally use virtual environments to mitigate)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST create the root directories: `book/`, `backend/`, `skills/`, `specs/`.
- **FR-002**: The system MUST install Docusaurus 3.9 (Classic preset) within the `book/` directory.
- **FR-003**: The system MUST set up a Python 3.12 environment in `backend/` with FastAPI, Uvicorn, and Qdrant Client installed.
- **FR-004**: The system MUST create a `main.py` file in `backend/` with a basic "Hello World" endpoint.
- **FR-005**: The system MUST create placeholder files `ingest.py` and `publish.py` in the `skills/` directory.
- **FR-006**: The system MUST ensure `CLAUDE.md` and essential `.specify/` templates are present and correctly configured.

### Key Entities *(include if feature involves data)*

- **Project Structure**: The arrangement of directories and files that constitute the project.
- **Dependencies**: External libraries and tools required for the project (Docusaurus, FastAPI, Uvicorn, Qdrant Client).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A new developer can initialize the project structure and all core dependencies within 15 minutes by following documented steps.
- **SC-002**: All foundational directories (`book/`, `backend/`, `skills/`, `specs/`) are created successfully upon initialization.
- **SC-003**: The Docusaurus site in `book/` successfully builds without errors on initial setup.
- **SC-004**: The FastAPI backend in `backend/` successfully starts and serves the "Hello World" endpoint.
- **SC-005**: All placeholder skill files (`ingest.py`, `publish.py`) are present in the `skills/` directory.
