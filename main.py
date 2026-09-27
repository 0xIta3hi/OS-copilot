import json
from typing import Any

from plugin_loaded import PLUGIN_REGISTRY
from plugin_registry import PluginRegistry

SYSTEM_PROMPT = """
You are a Windows OS Automation Agent.
You do NOT respond with conversation, apologies, or explanations.
You ONLY respond with executable JSON.

Available tools:
{tools}

Return exactly this format:
{
    "tool": "<tool name>",
    "parameters": {
        "<parameter>": "<value>"
    }
}

If the user input is not a command (e.g., "Hi"), return:
{
    "tool": "none",
    "parameters": {}
}
"""


def _parse_command(reply: str) -> dict[str, Any]:
    clean_json = reply.replace("```json", "").replace("```", "").strip()
    command = json.loads(clean_json)
    if not isinstance(command, dict):
        raise ValueError("LLM response must be a JSON object")
    return command


def process_command(user_input: str, registry: PluginRegistry | None = None) -> Any:
    import ollama

    registry = registry or PLUGIN_REGISTRY
    print(f"User said: {user_input}")
    response = ollama.chat(model="phi3:mini", messages=[
        {'role': 'system', 'content': SYSTEM_PROMPT.replace("{tools}", registry.describe())},
        {'role':'user', 'content':user_input},
    ])
    reply = response['message']['content']
    print(f"LLM said: {reply}")

    try:
        command = _parse_command(reply)
        tool_name = command.get("tool")
        if tool_name == "none":
            print("Agent: (Ignored conversational input)")
            return None
        if not isinstance(tool_name, str) or not registry.has_tool(tool_name):
            raise ValueError(f"Unknown tool selected by LLM: {tool_name}")
        parameters = command.get("parameters", {})
        if not isinstance(parameters, dict):
            raise ValueError("Tool parameters must be a JSON object")
        result = registry.execute(tool_name, parameters)
        print(f"Agent result: {result}")
        return result
    except json.JSONDecodeError:
        print("Error: LLM failed to generate valid json")
    except Exception as e:
        print(f"Error executing tool: {e}")

if __name__ == "__main__":
    process_command("Find the docker file for intelowl project.")