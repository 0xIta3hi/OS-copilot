import customtkinter as ctk
import keyboard
import threading

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
        print(f"Agent processing: {user_input}")
        
        self.entry.delete(0, 'end') # Clear box
        self.hide_window()

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