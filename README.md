# 🕵️ OS Copilot (Local)

**A privacy-first, open-source AI Agent for Windows that runs entirely on your machine.**

OS Copilot is a **native Windows automation tool** designed to replace cloud-based assistants like Microsoft Copilot. It lives in your background processes, wakes up with a hotkey, and interacts with your file system using a local LLM. **No data leaves your device.**

## ✨ Features

- **⚡ Instant Access:** Triggered globally via `Ctrl + Space` (Spotlight/Raycast style).
    
- **🔒 Privacy First:** Runs on **Ollama** (Llama 3) locally. Your files are never sent to OpenAI/Anthropic.
    
- **🧠 Intelligent Search:** Finds files by context and path keywords (e.g., "intelowl docker" finds `.../IntelOwl/Dockerfile`).
    
- **🛠️ Agentic Tool Use:** The LLM doesn't just chat; it executes Python functions to search, read, and open files.
    
- **🛡️ Safety Rails:** Large files are truncated automatically with user prompts to continue reading, preventing memory crashes.
    

## 🛠️ Tech Stack

- **Core:** Python 3.11 (Native Windows)
    
- **GUI:** `customtkinter` (Modern, dark-mode overlay)
    
- **LLM Backend:** `ollama` (Running `llama3`)
    
- **Input Handling:** `keyboard` (Global hotkeys via background threading)
    

## 🚀 Installation

### 1. Prerequisites

- **Python 3.10+** installed.
    
- **[Ollama](https://ollama.com/)** installed and running.
    
- Pull the Llama 3 model:
    
    PowerShell
    
    ```
    ollama pull llama3
    ```
    

### 2. Clone & Install

Bash

```
git clone https://github.com/yourusername/os-copilot.git
cd os-copilot

# Create a virtual environment (Recommended)
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install customtkinter keyboard ollama
```

## 🎮 Usage

1. **Start the Agent:**
    
    Bash
    
    ```
    python main.py
    ```
    
    _(The script will hide itself and run in the background)_
    
2. **Trigger the UI:** Press **`Ctrl + Space`**.
    
3. **Command Examples:**
    
    - _"Where is the dockerfile for the intelowl project?"_
        
    - _"Open my resume PDF."_
        
    - _"Read the error logs in the downloads folder."_
        

## 🧩 Architecture

The system uses a **ReAct (Reason + Act)** loop approach:

1. **Listener:** A background thread waits for the hotkey.
    
2. **Input:** User types a natural language query.
    
3. **Reasoning:** Llama 3 receives the query + a System Prompt forcing it to output **JSON**.
    
4. **Action:** The Python script parses the JSON, executes the corresponding tool (`search_files`, `read_files`, etc.), and returns the output.
    

## ⚠️ Disclaimer

**Use with caution.** This agent executes code on your local machine. While it currently only has read/search permissions, future versions with "Edit" or "Delete" capabilities should be monitored closely. I am not responsible if the agent hallucinates and you accidentally delete your homework folder.

## 🗺️ Roadmap

- [x] Basic GUI & Hotkey Listener
    
- [x] JSON Function Calling (Search, Read, Open)
    
- [ ] **Conversation Memory** (Context retention between turns)
    
- [ ] **File Editing** (Apply diffs/patches to code)
    
- [ ] **RAG Integration** (Chat with your PDF/Notes content)
    

## 🤝 Contributing

Pull requests are welcome! If you want to teach this agent new tricks (new tools), feel free to open an issue.

## 📄 License

MIT