# Template Spec: Add RAG Agent With FunctionTool

## Goal

Create a RAG Agent that wraps an existing RAG function using `FunctionTool`.

## Fill these placeholders

- Backend root: `{{backend_root}}`
- Agents module path: `{{agents_module}}` (e.g. `{{backend_root}}/agents/rag_agent.py`)
- RAG module: `{{rag_module}}` (e.g. `{{backend_root}}/rag/service.py`)
- RAG function name: `{{rag_function_name}}` (signature: `(query: str) -> str`)
- Model id: `{{model_id}}`

## Requirements

1. In `{{agents_module}}`:

   - Import:

     - `FunctionTool`, `RunContextWrapper` from `agents`.
     - `BaseModel` from `pydantic`.
     - The existing RAG function from `{{rag_module}}`. [web:21][web:24]

   - Define a Pydantic model for tool args, for example:

     - `class RagArgs(BaseModel): query: str`

   - Define an async tool handler:

     - Signature: `async def run_rag_tool(ctx: RunContextWrapper[Any], args: str) -> str`
     - Inside:
       - Parse args via `RagArgs.model_validate_json(args)`.
       - Call the existing RAG function with the parsed query.
       - Return the answer string.

   - Create a `FunctionTool`:

     - `name`: e.g. `"rag_qa"`.
     - `description`: what the tool does.
     - `params_json_schema`: from `RagArgs.model_json_schema()`.
     - `on_invoke_tool`: set to the handler.

   - Create an `Agent`:

     - With `model={{model_id}}`.
     - `instructions` describing that it should use the RAG tool when needed.
     - `tools=[rag_tool]`.

2. Optionally provide a helper:

   - `async def run_rag_agent(question: str) -> str: ...`

## Constraints

- Do NOT change the body of `{{rag_function_name}}`; only call it.
- Keep the Agents SDK logic in `{{agents_module}}` so it can be reused.
