import platform
import subprocess
import os
from openai import OpenAI
from composio import Composio
from dotenv import load_dotenv

load_dotenv()

composio = Composio()


def read_files(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            content = f.read(10000)
            if len(content) == 10000:
                print("[!] File too long to read showing first 10000 character")
                print(content)

                user_agreement = input("Do you want to read the rest of file (y/n)")
                if user_agreement in ["y", "yes"]:
                    remaining_content = f.read()
                    print(remaining_content)
                    return content + remaining_content
                else:
                    return content + "__Truncated__"
            return content
    except FileNotFoundError:
        print(f"The requested file not found")
    except Exception as e:
        print(f"The following ran occured : {e}")

def open_files(file_name):
    try:
        os.startfile(file_name)
        return f"File Opened: {file_name}"
    except Exception as e:
        return f"Error : {e}"


# Implementing composio tools logic.
# initializing the client.
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)

toolset = "Tool set yet to be decided."

tools = toolset.get_tools(apps=[App.GITHUB])

messages = [
    {
        "role":"user",
        "content":"Star the repository : 0xIta3hi/OS-copilot on Github"
    }
]

response = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",
    messages=messages,
    tools=tools,
    tool_choice="auto",
)
tool_result = toolset.handle_tool_calls(response)
print("Tool Execution Result:", tool_result)


