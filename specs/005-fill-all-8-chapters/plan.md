# Implementation Plan: Fill 8 Chapters

**Branch**: `005-fill-all-8-chapters` | **Date**: 2025-11-30 | **Spec**: [./../spec.md](specs/005-fill-all-8-chapters/spec.md)
**Input**: Feature specification from `/specs/005-fill-all-8-chapters/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

The primary requirement is to populate 8 existing Docusaurus chapter folders by recursively iterating through *all* `.md` files within each folder. For each `.md` file, the plan is to extract the matching section from `specs/input/syllabus.md` based on the filename, expand it into high-quality, relevant content (e.g., 500+ words), and then overwrite the specific `.md` file. The goal is to ensure no markdown file remains empty, utilizing the `content-writer` agent with a "Pedagogue" persona.

## Technical Context

**Language/Version**: Python 3.10+ (for content-writer agent execution and file system operations)
**Primary Dependencies**: `content-writer` agent, Docusaurus (target output format), OS-level file system utilities (for listing `.md` files).
**Storage**: Filesystem (for `index.md`, `learning-outcomes.md`, `summary.md`, and other `.md` files)
**Testing**: Manual review of word count and style, automated file existence/overwrite checks, and verification that no `.md` files remain empty.
**Target Platform**: Docusaurus-generated static site.
**Project Type**: Book content generation within an existing Docusaurus project.
**Performance Goals**: Efficient content generation and file writing across multiple `.md` files per chapter.
**Constraints**:
- Do NOT create new chapter folders.
- Each *individual* `.md` file within a chapter folder must be populated with content (e.g., 500+ words, unless otherwise specified by content).
- Style: Pedagogue (Simple English).
- Ensure NO file remains empty.
**Scale/Scope**: 8 chapters, each potentially containing multiple `.md` files.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Project Vision & Governance**: Adheres to the workflow `sp.specify` -> `sp.plan` -> `sp.implement`.
- **Mandatory Tech Stack**: Utilizes Docusaurus for frontend output and Python for agent execution. Qdrant/Neon are not directly involved in *this* content generation phase, but the overall project leverages them.
- **Content Standards**: Requires generated content to be Flesch-Kincaid Grade 10-12, and AI-generated. This plan further refines the style to "Pedagogue" (Simple English) for this specific task.

## Project Structure

### Documentation (this feature)

```text
specs/005-fill-all-8-chapters/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
book/
└── docs/
    ├── chapter-1:-introduction-to-physical-ai-&-humanoid-robotics/
    │   ├── index.md        # Target for content
    │   └── learning-outcomes.md # Example target
    ├── chapter-2:-ros-2-fundamentals/
    │   ├── index.md        # Target for content
    │   └── concepts.md     # Example target
    ├── chapter-3:-robot-simulation/
    │   └── index.md        # Target for content
    ├── chapter-4:-nvidia-isaac-platform/
    │   └── index.md        # Target for content
    ├── chapter-5:-humanoid-robot-development/
    │   └── index.md        # Target for content
    ├── chapter-6:-conversational-robotics/
    │   └── index.md        # Target for content
    ├── chapter-7:-assessments/
    │   └── index.md        # Target for content
    └── chapter-8:-hardware-requirements/
        └── index.md        # Target for content
```

**Structure Decision**: The content will be generated and written directly into *all* existing `.md` files within the `book/docs/chapter-X/` directories, aligning with the Docusaurus frontend structure. The agent will discover these files and populate them based on their filenames and relevant syllabus sections.
