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