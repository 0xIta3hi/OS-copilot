import ollama
import json
from file_search import *

SYSTEM_PROMPT = """
You are a Windows OS Automation Agent.
You do NOT respond with conversation, apologies, or explanations.
You ONLY respond with executable JSON.

Available Tools:
1. search_files(keyword): Search for files in the home directory.

Format your response exactly like this:
{
    "tool": "search_files",
    "parameters": {
        "keyword": "example.txt"
    }
}

If the user input is not a command (e.g., "Hi"), return:
{
    "tool": "none",
    "parameters": {}
}
"""

def process_command(user_input):
    print(f"User said: {user_input}")
    response = ollama.chat(model="phi3:mini", messages=[
        {'role':'system', 'content':SYSTEM_PROMPT},
        {'role':'user', 'content':user_input},
    ])
    reply = response['message']['content']
    print(f"LLM said: {reply}")

    try:
        clean_json = reply.replace("```json", "").replace("``", "").strip()
        command = json.loads(clean_json)

        if command.get("tools") == "search_files":
            query = command['parameters']['keyword']
            print(f"Agent action: searching for {query}")

            files_found = search_files(query)
            if files_found:
                print("Found files")
                for f in files_found:
                    print(f" - {f}")
            else:
                print(f"No such file as {query}")
        elif command.get("tool") == "none":
            print("Agent: (Ignored conversational input)")
    except json.JSONDecodeError:
        print("Error: LLM failed to generate valid json")
    except Exception as e:
        print(f"Error executing tool: {e}")

if __name__ == "__main__":
    process_command("Find the docker file for intelowl project.")