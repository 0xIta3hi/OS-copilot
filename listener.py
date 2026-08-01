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


