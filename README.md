# OS Copilot (Local) 🤖💻

### _Privacy-First, Local-LLM Automation for Windows_

OS Copilot is an open-source, native Windows agent designed to give users the power of an AI assistant without the privacy trade-offs of cloud-based services. It runs **100% locally** via Ollama, allowing it to search, read, and interact with your file system without a single byte of data leaving your device.

## ⚡ Why OS Copilot?

Current AI assistants require "Everything Access" to your cloud data. OS Copilot flips the script:

- **Total Privacy:** Uses `Llama 3` running locally. Your personal documents, code, and logs remain on your disk.
    
- **Native Windows Integration:** Built with a "Spotlight-style" global overlay (`Ctrl + Space`) for instant access from any application.
    
- **Agentic Capabilities:** It doesn't just chat; it uses **ReAct (Reason + Act) prompting** to execute Python-based "Tools" for file system operations.
    

## 🛠️ The "Agentic" Workflow

OS Copilot operates on a continuous feedback loop:

1. **Observation:** User asks: "Find my resume and tell me the last job I listed."
    
2. **Reasoning:** The LLM decides it needs to use the `search_files` tool first.
    
3. **Action:** The Python backend executes the search and returns paths to the LLM.
    
4. **Refinement:** The LLM then chooses the `read_file` tool to extract the job info.
    
5. **Final Output:** AI presents the answer to the user in the UI overlay.
    

## 🛠️ Technical Stack

- **Backend:** Python 3.11 with custom threading for the global hotkey listener.
    
- **GUI:** `customtkinter` – Provides a modern, GPU-accelerated, dark-mode interface.
    
- **Inference Engine:** `Ollama` (Running `Llama 3`).
    
- **Tooling:** Custom Python OS wrappers for secure file searching and reading.
    

## 🛡️ Safety & Guardrails

Because the agent can access the file system, security is built into the core:

- **Read-Only Default:** Currently, the agent is restricted to `Search`, `Read`, and `Open` operations. No `Delete` or `Edit` permissions are granted by default.
    
- **Context Truncation:** To prevent LLM "memory crashes," large files are automatically summarized or truncated before being sent to the LLM.
    
- **User-in-the-Loop:** For sensitive operations like opening an executable, the system can be configured to require manual confirmation.
    

## 🚀 Getting Started

1. **Install Ollama:** Download from [ollama.com](https://ollama.com "null").
    
2. **Pull Model:** `ollama pull llama3`
    
3. **Clone & Run:**
    

```
git clone [https://github.com/yourusername/os-copilot.git](https://github.com/yourusername/os-copilot.git)
pip install -r requirements.txt
python main.py
```

## Enhancements:
    - Case Sensitive detection.
    - The Agent can't yet think through vague inputs.
    - Latency reduction.

_Press `Ctrl + Space` to summon the assistant._

_Empowering users with private, local intelligence._
