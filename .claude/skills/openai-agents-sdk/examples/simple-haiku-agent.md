# Example: Simple Haiku Agent (Decorator Tool)

This example shows the canonical pattern for creating an `Agent` with a simple function tool. [web:21][web:42]

```python

from agents import Agent, ModelSettings, function_tool

@function_tool
def get_weather(city: str) -> str:
"""returns weather info for the specified city."""
return f"The weather in {city} is sunny"

agent = Agent(
name="Haiku agent",
instructions="Always respond in haiku form",
tools=[get_weather],
)
```

**What this teaches Claude:**

- Use `@function_tool` on small, synchronous helper functions.
- Pass the decorated function directly in the `tools` list.
- Keep `instructions` focused and role‑like (system‑style). [web:21][web:42]

When adapting to a project, the spec will change:
- Agent name
- Instructions
- Model id
- Actual tool functions

