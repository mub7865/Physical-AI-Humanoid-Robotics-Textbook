# OpenAI Agents SDK Skill

## Purpose

This skill encodes reusable intelligence for working with the **OpenAI Agents Python SDK**:
- Creating `Agent` objects with models and instructions.
- Defining tools using both `@function_tool` and `FunctionTool`.
- Using `RunContextWrapper` in async tool handlers. [web:21][web:42]

It should work across any Python backend or script. The spec will provide project‑specific paths; this skill only provides patterns.

## What this skill must know

- How to create a simple Agent:

  - `from agents import Agent, ModelSettings, function_tool` etc. [web:21][web:42]

- How to define tools in two ways:

  1. Decorator style:

     - `@function_tool` on a plain Python function.
     - Pass that function instance into `tools=[...]` when constructing the Agent.

  2. Low‑level `FunctionTool` style:

     - Define a `BaseModel` args schema.
     - Implement `async def run_function(ctx: RunContextWrapper[Any], args: str) -> str`.
     - Create `FunctionTool(...)` with `params_json_schema` and `on_invoke_tool`. [web:21][web:24]

- How to keep this logic isolated in `agents/` or similar modules so it can be reused across projects.

## How this skill should be used

Specs that use this skill should:

- Provide placeholders like:
  - `{{backend_root}}`
  - `{{agents_module}}`
  - `{{rag_module}}`
  - `{{rag_function_name}}`
  - `{{model_id}}`

- Describe **what kind of agent** is needed:
  - Simple chat agent
  - RAG agent that calls an existing function
  - Multi‑tool or specialist agent

This skill then guides Claude to:

1. Create or update an Agents module.
2. Define one or more tools.
3. (Optionally) Expose a public function that higher layers (HTTP, CLI, etc.) can call.

## Guardrails

When used on real projects, the spec should state:

- Do NOT:
  - Delete or rename existing modules or endpoints.
  - Rewrite existing domain logic/RAG logic; always wrap as tools.
- DO:
  - Place Agents SDK code under a focused directory (e.g. `{{backend_root}}/agents/`).
  - Keep agents and tools small, composable, and testable.

## Reusability

The same patterns from the `examples/` and `templates/` in this skill should be reusable across:

- Different web frameworks (FastAPI, Flask, Django REST).
- Pure Python scripts.
- Different domains (RAG textbooks, CRUD apps, utilities).

Only the paths, model names, and business functions change; the **Agents SDK wiring pattern stays the same**. [web:21][web:42]
