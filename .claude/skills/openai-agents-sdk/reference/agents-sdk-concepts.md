# OpenAI Agents SDK – Core Concepts

Use these as the mental model this skill relies on. [web:21][web:42]

- **Agent**
  - Combines: model, instructions, tools, and optional guardrails.
  - Represents a “smart worker” with a clear role.

- **Tools**
  - Functions the agent can call to do real work (code, I/O, external systems).
  - Two main patterns:
    - `@function_tool` decorator on simple functions.
    - `FunctionTool` with explicit `params_json_schema` and async handlers using `RunContextWrapper`. [web:21][web:24]

- **RunContextWrapper**
  - Context passed to tools so they can access run metadata or shared state.

- **Schemas via Pydantic**
  - Use `BaseModel` and `.model_json_schema()` to define tool argument schemas. [web:21][web:24]

This skill expects Claude to:
- Use these patterns when implementing or refactoring Agents in any project.
- Prefer composition (wrap existing logic into tools) over rewriting logic.
