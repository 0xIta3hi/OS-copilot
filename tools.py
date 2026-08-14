import platform
import subprocess
import os
from composio import Composio
import asyncio
from composio_llamaindex import LlamaIndexProvider
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.llms.openai import OpenAI

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
composio = Composio(provider=LlamaIndexProvider())
llm = OpenAI(model="gpt-5.2")

session = composio.create(user_id="user_1337")
tools = session.tools()
agent = FunctionAgent(tools=tools, llm=llm)

async def main():
    result = await agent.run(
        user_msg="send an email to john@example.com with the subject composio email be working !!!"
    )
    print(result)

asyncio.run(main())


