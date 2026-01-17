import customtkinter as ctk
import keyboard
import threading
import ollama
from file_search import *
import json
class AgentGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("OS Copilot")
        self.geometry("600x100")
        self.resizable(False, False)
        
        # Remove the title bar (Make it look like a tool, not a window)
        self.overrideredirect(True) 
        
        # Center on screen (Rough calculation)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - 300
        y = (screen_height // 3)  # Top third looks better
        self.geometry(f"600x80+{x}+{y}")

        # The Input Field
        self.entry = ctk.CTkEntry(
            self, 
            placeholder_text="What do you need, boss?", 
            width=580, 
            height=60,
            font=("Arial", 18)
        )
        self.entry.pack(pady=10, padx=10)
        
        # Bind "Enter" key to run the agent
        self.entry.bind("<Return>", self.run_agent_task)
        
        # Bind "Escape" to close/hide
        self.bind("<Escape>", self.hide_window)

    def show_window(self):
        self.deiconify() # Un-hide
        self.entry.focus_set() # Focus text box immediately
        self.attributes("-topmost", True) # Force to top

    def hide_window(self, event=None):
        self.withdraw() # Hide (but keep running)

    def run_agent_task(self, event=None):
            user_input = self.entry.get()
            if not user_input: return

            print(f"\n[You]: {user_input}")
            self.entry.delete(0, 'end')
            self.hide_window()
            threading.Thread(target=self.agent_processing, args=(user_input,)).start()

    def agent_processing(self, prompt):
        print("[+] Sent to Friday.")
        try:
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
            response = ollama.chat(
                model="phi3:mini",
                messages=[
                    {'role':'system', 'content':SYSTEM_PROMPT},
                    {'role':'user', 'content':prompt}
                ]
            )
            reply = response['message']['content']
            print("Raw reply : \n",reply)
            start_indx = reply.find('{')
            end_indx = reply.rfind('}')
            if start_indx != -1 and end_indx != -1:
                clean_json = reply[start_indx : end_indx + 1]
                print( "Json After cleaning: \n", clean_json)
                command = json.loads(clean_json)
                print("Selected command:\n", command)
            else:
                print('Error: No brackets found.')
            if command.get('tools') == "search_files":
                query = command['parameters']['keyword']
                print("Recieved query:\n", query)
                print(f"Agent action: searching for {query}")
                files_found = search_files(query)
                if files_found:
                    print("[+] Found these files:")
                    for f in files_found:
                        print(f" - {f}")
                else:
                    print("No such file in the system.")
            elif command.get("tool") == "none":
                print("Agent: (Ignored conversational input)")
        except json.JSONDecodeError as e:
            print(f"Error: LLM failed to generate valid json. {e}")
        except Exception as e:
            print(f"Failed due to {e}")

# --- The Listener Thread ---
def start_listener(app):
    # This runs in background waiting for Ctrl+Space
    keyboard.add_hotkey('ctrl+space', lambda: app.after(0, app.show_window))
    keyboard.wait()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = AgentGUI()
    
    # Hide immediately on start
    app.withdraw()
    
    # Start the hotkey listener in a separate thread so GUI doesn't freeze
    listener_thread = threading.Thread(target=start_listener, args=(app,), daemon=True)
    listener_thread.start()
    
    app.mainloop()