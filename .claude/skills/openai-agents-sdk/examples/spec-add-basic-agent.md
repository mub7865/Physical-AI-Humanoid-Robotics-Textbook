# Template Spec: Add Basic Agent Using @function_tool

## Goal

Create a simple OpenAI Agent using the `@function_tool` decorator in this project. No project‑specific names are hardcoded here.

## Fill these placeholders

- Backend root: `{{backend_root}}`
- Agents module path: `{{agents_module}}` (e.g. `{{backend_root}}/agents/basic_agent.py`)
- Model id: `{{model_id}}` (e.g. `gpt-4.1-mini`)

## Requirements

1. Create or update `{{agents_module}}` so that it contains:

   - An example tool using `@function_tool`, similar in structure to:

     - Takes simple typed args (e.g. `city: str`).
     - Returns a string result.

   - An `Agent` instance:

     - `name`: short identifier for this agent.
     - `instructions`: clear description of behaviour.
     - `model`: set to `{{model_id}}`.
     - `tools`: list containing the decorated tool. [web:21][web:42]

2. Optionally expose a helper like:

   - `def run_basic_agent(message: str) -> str: ...`

   which:
   - Prepares a messages list.
   - Invokes the Agent through the Agents SDK.
   - Returns the final text answer.

## Constraints

- Keep the tool logic small and self‑contained.
- Do not tie this spec to any particular framework.
