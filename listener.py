import customtkinter as ctk
import keyboard
import threading
import ollama
import json
# IMPORT YOUR TOOLS
from file_search import search_files
from tools import read_files, open_files 

class AgentGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("OS Copilot")
        self.geometry("600x100")
        self.resizable(False, False)
        self.overrideredirect(True) 
        
        # Center on screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - 300
        y = (screen_height // 3) 
        self.geometry(f"600x80+{int(x)}+{int(y)}")

        # The Input Field
        self.entry = ctk.CTkEntry(
            self, 
            placeholder_text="Qwen is listening...", 
            width=580, 
            height=60,
            font=("Arial", 18)
        )
        self.entry.pack(pady=10, padx=10)
        
        self.entry.bind("<Return>", self.run_agent_task)
        self.bind("<Escape>", self.hide_window)

    def show_window(self):
        self.deiconify() 
        self.entry.focus_set() 
        self.attributes("-topmost", True) 

    def hide_window(self, event=None):
        self.withdraw() 

    def run_agent_task(self, event=None):
            user_input = self.entry.get()
            if not user_input: return

            print(f"\n[You]: {user_input}")
            self.entry.delete(0, 'end')
            self.hide_window()
            threading.Thread(target=self.agent_processing, args=(user_input,)).start()

    def agent_processing(self, prompt):
        print("[+] Sent to Qwen.")
        try:
            # UPDATED SYSTEM PROMPT FOR QWEN
            SYSTEM_PROMPT = """
            You are a Windows OS Automation Agent.
            You do NOT respond with conversation. You ONLY respond with executable JSON.

            Available Tools:
            1. search_files(keyword): Search for files by name/path.
            2. read_files(path): Read the content of a file (Code, Logs, Text).
            3. open_files(path): Open a file in the default Windows app.

            Example Response:
            { "tool": "search_files", "parameters": { "keyword": "notes.txt" } }
            
            If the user input is not a command, return:
            { "tool": "none", "parameters": {} }
            """
            
            response = ollama.chat(
                model="qwen2.5-coder", # Make sure this matches your pull name
                messages=[
                    {'role':'system', 'content':SYSTEM_PROMPT},
                    {'role':'user', 'content':prompt}
                ],
                options={'temperature': 0} # Keep it strict
            )
            
            reply = response['message']['content']
            print("Raw reply : \n", reply)
            
            # --- ROBUST JSON EXTRACTION ---
            start_indx = reply.find('{')
            end_indx = reply.rfind('}')
            
            if start_indx != -1 and end_indx != -1:
                clean_json = reply[start_indx : end_indx + 1]
                command = json.loads(clean_json)
                print("Selected command:\n", command)
                
                tool_name = command.get('tool')
                
                # --- TOOL LOGIC ---
                
                # 1. SEARCH
                if tool_name == "search_files":
                    query = command['parameters']['keyword']
                    print(f"Agent action: Searching for '{query}'...")
                    found = search_files(query)
                    if found:
                        print("[+] Found files:")
                        for f in found:
                            print(f" - {f}")
                    else:
                        print("[-] No files found.")

                # 2. READ
                elif tool_name == "read_files":
                    path = command['parameters']['path']
                    print(f"Agent action: Reading '{path}'...")
                    content = read_files(path)
                    print(f"\n--- FILE CONTENT ---\n{content}\n--------------------")

                # 3. OPEN
                elif tool_name == "open_files":
                    path = command['parameters']['path']
                    print(f"Agent action: Opening '{path}'...")
                    result = open_files(path)
                    print(result)

                elif tool_name == "none":
                    print("Agent: (Ignored conversational input)")
                
                else:
                    print(f"[!] Error: Qwen tried to use unknown tool: {tool_name}")

            else:
                print('Error: No JSON brackets found in response.')

        except json.JSONDecodeError as e:
            print(f"Error: JSON parsing failed. {e}")
        except Exception as e:
            print(f"System Error: {e}")

# --- The Listener Thread ---
def start_listener(app):
    keyboard.add_hotkey('ctrl+space', lambda: app.after(0, app.show_window))
    keyboard.wait()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = AgentGUI()
    app.withdraw()
    listener_thread = threading.Thread(target=start_listener, args=(app,), daemon=True)
    listener_thread.start()
    print("OS Copilot (Qwen Edition) is running...")
    app.mainloop()