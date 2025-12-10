# Example: FunctionTool With RunContext and Pydantic

This example shows how to use `FunctionTool` with a typed arguments schema and `RunContextWrapper`. [web:21][web:24]

```python

from typing import Any

from pydantic import BaseModel

from agents import RunContextWrapper, FunctionTool

def do_some_work(data: str) -> str:
return "done"

class FunctionArgs(BaseModel):
username: str
age: int

async def run_function(ctx: RunContextWrapper[Any], args: str) -> str:
parsed = FunctionArgs.model_validate_json(args)
return do_some_work(data=f"{parsed.username} is {parsed.age} years old")

tool = FunctionTool(
name="process_user",
description="Processes extracted user data",
params_json_schema=FunctionArgs.model_json_schema(),
on_invoke_tool=run_function,
)
```


**What this teaches Claude:**

- Use `BaseModel` for tool argument schemas.
- Use `RunContextWrapper[Any]` in async handlers to access context if needed.
- Use `model_validate_json` to parse the tool arguments.
- Pass `params_json_schema` into `FunctionTool` so the agent can call it correctly. [web:21][web:24]
