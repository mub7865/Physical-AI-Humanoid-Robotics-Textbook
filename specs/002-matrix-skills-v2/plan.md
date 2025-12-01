# Implementation Plan: Reusable Intelligence Layer (5 Critical Skills)

**Branch**: `002-matrix-skills-v2` | **Date**: 2025-11-29 | **Spec**: [./specs/002-matrix-skills-v2/spec.md](specs/002-matrix-skills-v2/spec.md)
**Input**: Feature specification from `/specs/002-matrix-skills-v2/spec.md`

## Summary

This plan outlines the implementation of a standardized folder structure and initial Python logic for 5 critical AI-native skills: Curriculum Designer, The Pedagogue, Brain Builder, Librarian, and Publisher. The goal is to establish a reusable intelligence layer by defining these skills with their respective goals, scripts, and underlying logic, while ensuring adherence to the project's mandated technology stack and folder structure.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: `FastAPI`, `Uvicorn`, `openai`, `tiktoken`, `python-dotenv`, `qdrant-client`
**Storage**: Qdrant Cloud (for vector embeddings), Neon Serverless Postgres (for chat history & user data)
**Testing**: `pytest`
**Target Platform**: Linux server
**Project Type**: Web application (Frontend + Backend)
**Performance Goals**: N/A (focus on structure and initial logic)
**Constraints**: Strict adherence to the specified `.claude/skills/` folder structure.
**Scale/Scope**: Definition and initial implementation of 5 core reusable AI agent skills.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **ZERO VIBE CODING:** Development is forbidden without an existing `spec.md` and `plan.md`. (Passed: `spec.md` exists and this `plan.md` is being generated).
- [x] **Workflow:** `sp.specify` (Define) -> `sp.plan` (Architect) -> `sp.implement` (Code). (Passed: Following the prescribed workflow).
- [x] **Mandatory Tech Stack:** Adherence to Python 3.10+, FastAPI, OpenAI Agents SDK, Qdrant. (Passed: Dependencies are aligned with the constitution).
- [x] **The "Matrix" Protocol (Reusable Intelligence):** Agent Skills located in `skills/`. (Passed: This plan directly implements the structure for these skills).

## Project Structure

### Documentation (this feature)

```text
specs/002-matrix-skills-v2/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command) - N/A for this phase
├── data-model.md        # Phase 1 output (/sp.plan command) - N/A for this phase
├── quickstart.md        # Phase 1 output (/sp.plan command) - N/A for this phase
├── contracts/           # Phase 1 output (/sp.plan command) - N/A for this phase
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
.claude/skills/
├── curriculum-designer/
│   ├── SKILL.md
│   └── scripts/
│       └── structure.py
├── pedagogue/
│   ├── SKILL.md
│   └── scripts/
│       └── teach.py
├── brain-builder/
│   ├── SKILL.md
│   └── scripts/
│       └── scaffold.py
├── librarian/
│   ├── SKILL.md
│   └── scripts/
│       └── ingest.py
└── publisher/
    ├── SKILL.md
    └── scripts/
        └── publish.py

backend/
└── requirements.txt
```

**Structure Decision**: The `.claude/skills/` directory will house each skill in its own sub-directory, each containing a `SKILL.md` and a `scripts/` directory with the primary Python script. The `backend/requirements.txt` file will be updated with new dependencies.

## Implementation Steps

### 1. Update `backend/requirements.txt`

Add the following dependencies to `backend/requirements.txt`:
```
openai
tiktoken
python-dotenv
qdrant-client
```

### 2. Implement Curriculum Designer (`.claude/skills/curriculum-designer/scripts/structure.py`)

**Goal**: Read `specs/input/syllabus.md`, extract headers (`#`), create folders/files in `book/docs/`.
**Code Structure**:
```python
import os

def create_book_structure(syllabus_path, output_base_path):
    with open(syllabus_path, 'r') as f:
        syllabus_content = f.readlines()

    current_chapter = None
    for line in syllabus_content:
        if line.startswith('# '):  # Main chapter
            chapter_title = line.strip('# ').strip()
            chapter_slug = chapter_title.lower().replace(' ', '-')
            chapter_dir = os.path.join(output_base_path, chapter_slug)
            os.makedirs(chapter_dir, exist_ok=True)
            current_chapter = chapter_dir
            # Create index.md for chapter
            with open(os.path.join(chapter_dir, 'index.md'), 'w') as f:
                f.write(f'# {chapter_title}\n\n')
        elif line.startswith('## ') and current_chapter:  # Section within chapter
            section_title = line.strip('## ').strip()
            section_slug = section_title.lower().replace(' ', '-')
            with open(os.path.join(current_chapter, f'{section_slug}.md'), 'w') as f:
                f.write(f'# {section_title}\n\n')
        # Add logic to generate sidebars.ts (placeholder for now)
    print(f"Generated book structure in {output_base_path}")

if __name__ == "__main__":
    syllabus_path = "specs/input/syllabus.md"
    output_base_path = "book/docs/"
    create_book_structure(syllabus_path, output_base_path)
```

### 3. Implement The Pedagogue (`.claude/skills/pedagogue/scripts/teach.py`)

**Goal**: Ensure content is "Beginner to Intermediate" friendly. Use `openai.Client` to re-write input text with analogies and simplified language.
**Code Structure**:
```python
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def simplify_text(text):
    prompt = f"""
    Rewrite the following text for a beginner to intermediate audience.
    Include real-world analogies, simplify jargon, and generate 3-5 key takeaways
    and 2-3 quiz questions.

    Original Text:
    {text}
    """
    response = client.chat.completions.create(
        model="gpt-4o",  # or another suitable model
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    sample_text = "The quantum entanglement phenomenon describes how two particles can become linked..."
    simplified_content = simplify_text(sample_text)
    print(simplified_content)
```

### 4. Implement Brain Builder (`.claude/skills/brain-builder/scripts/scaffold.py`)

**Goal**: Generate OpenAI Agent SDK code. Create a template string for an OpenAI Agent `Worker` class and write it to a new file.
**Code Structure**:
```python
import os

def scaffold_agent(agent_name, output_dir="backend/agents/"):
    worker_template = f"""
import openai
from openai_agents import Worker

class {agent_name.capitalize()}Worker(Worker):
    def __init__(self):
        super().__init__("{agent_name}")

    @openai.tool
    def example_tool(self, input_data: str):
        """
        An example tool for the {agent_name} agent.
        """
        print(f"Example tool called with: {{input_data}}")
        return f"Processed: {{input_data.upper()}}"

if __name__ == "__main__":
    # Example usage:
    # agent = {agent_name.capitalize()}Worker()
    # print(agent.example_tool("hello world"))
    pass
"""
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{agent_name.lower()}_worker.py")
    with open(file_path, "w") as f:
        f.write(worker_template)
    print(f"Generated OpenAI Agent boilerplate for '{agent_name}' at {file_path}")

if __name__ == "__main__":
    scaffold_agent("DataProcessor")
```

### 5. Implement Librarian (`.claude/skills/librarian/scripts/ingest.py`)

**Goal**: Ingest content to Qdrant. Pure OpenAI Embeddings + Qdrant Upload (No LangChain).
**Code Structure**:
```python
import os
from openai import OpenAI
from qdrant_client import QdrantClient, models
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
qdrant_client = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))

COLLECTION_NAME = "book_content"

def get_embeddings(text):
    response = client.embeddings.create(
        input=[text],
        model="text-embedding-3-small" # or another suitable model
    )
    return response.data[0].embedding

def ingest_document(document_id, content, metadata=None):
    embedding = get_embeddings(content)
    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            models.PointStruct(
                id=document_id,
                vector=embedding,
                payload={"content": content, **(metadata or {})}
            )
        ]
    )
    print(f"Document {document_id} ingested into Qdrant.")

if __name__ == "__main__":
    # Example: Initialize collection (run once)
    # qdrant_client.recreate_collection(
    #     collection_name=COLLECTION_NAME,
    #     vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
    # )

    sample_content = "This is a sample paragraph about AI-Native books."
    ingest_document("sample_doc_1", sample_content, {"source": "test_ingest"})
```

### 6. Implement Publisher (`.claude/skills/publisher/scripts/publish.py`)

**Goal**: Deploy to GitHub Pages. `subprocess.run(["npm", "run", "build"])` + git commands.
**Code Structure**:
```python
import subprocess
import os

def publish_site():
    print("Building Docusaurus site...")
    try:
        subprocess.run(["npm", "run", "build"], check=True, cwd="book/")
        print("Docusaurus site built successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error building Docusaurus site: {e}")
        return

    print("Deploying to GitHub Pages...")
    try:
        # Placeholder for git deployment logic
        # This typically involves committing the build output and pushing to a specific branch (e.g., gh-pages)
        # For a full implementation, consider using gh-pages package or specific git commands.
        # Example:
        # subprocess.run(["git", "add", "-f", "book/build"], check=True)
        # subprocess.run(["git", "commit", "-m", "Deploy to GitHub Pages"], check=True)
        # subprocess.run(["git", "push", "origin", "gh-pages"], check=True)
        print("Deployment logic would go here. (e.g., git add, commit, push to gh-pages branch)")
        print("Site deployed successfully (placeholder).")
    except subprocess.CalledProcessError as e:
        print(f"Error deploying to GitHub Pages: {e}")

if __name__ == "__main__":
    publish_site()
```

## Complexity Tracking

No significant constitution violations requiring justification.
