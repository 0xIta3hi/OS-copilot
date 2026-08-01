"""
To-Do's:
    - define tool registry. (the dictionary which contains all the tools and their descriptions in a key value pair.)
    - write the logic for central llm agent to select a tool from the registry and output that. 
    - Final output: central LLM chooses the correct tool based on the given input prompt from the user.
"""

TOOL_REGISTRY = {
    "search_files":"searches for a specific file in the entire OS",
    "read_file":"Reads the specific file, takes arguments of path and filename.",
    "open_file":"opens the file.",
    "send_mail":"Sends a mail via gmail, takes arguments of content, subject, reciepent",
    "send_discord_message":"sends a discord message to a specific server and channel"
}

import ollama
import json
import os

def get_tool_choice(user_input: str) -> str | None:
    tool_list = "\n".join(f"- {name}: {desc}" for name, desc in TOOL_REGISTRY.items())
    SYSTEM_PROMPT = f""" You are a routing agent, Given a user input, pick a tool from this list: {tool_list}
                         Respond only with a json object of format : {{"tool":"<tool_name>"}}, nothing else.   
                         if no tools fit respond with : {{"tool":"none"}}.
    """
    response = ollama.chat(
        model="phi3:mini",
        messages=[
            {"role":"system", "content":SYSTEM_PROMPT},
            {"role":"user", "content":user_input}
        ],
        options={"temperature":0}
    )
    raw = response["message"]["content"].strip()
    try:
        parsed_json = json.loads(raw)
        tool = parsed_json.get("tool")
        print(f"tool selected : {tool}")
        return tool if tool in TOOL_REGISTRY else None
    except json.JSONDecodeError:
        print("LLM did not generate valid json.\n", raw)
        return None

if __name__ == "__main__":
    test_prompts = [
        "Find the file named report.pdf",
        "Read the file notes.txt from my Documents folder",
        "Open calculator.py",
        "Send an email to john@example.com saying hello",
        "Send a Discord message to the #general channel",
        "What's the weather today?"
    ]

    for prompt in test_prompts:
        tool = get_tool_choice(prompt)
        print(f"User: {prompt}")
        print(f"Chosen Tool: {tool}")
        print("-" * 40)
