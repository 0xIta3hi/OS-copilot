# OS Copilot

OS Copilot is a local Python agent that uses Ollama to translate natural-language requests into registered plugin actions. The current implementation provides a read-only local filesystem plugin and a small plugin registry designed for adding more platform integrations.

## How It Works

```text
User request
	|
	v
main.py -> Ollama returns a JSON tool command
	|
	v
plugin_loaded.py -> provides the active registry
	|
	v
plugin_registry.py -> validates and dispatches the tool
	|
	v
plugins/local_files.py -> performs the read-only filesystem action
```

Authentication is intentionally outside the plugin interface. Plugins expose platform actions; they do not need to know how authentication is configured.

## Current Features

The default `LocalFileSystem` plugin is registered with these tools:

- `file_search(keyword, path=".")`: recursively searches filenames.
- `open_file(filename, path=".")`: reads a UTF-8 text file.
- `file_system_manipulation(action, path=".")`: inspects a path with `exists`, `list`, or `info`.

The plugin confines paths to its configured root, defaults to the current user's home directory, and limits search results to 50 entries.

## Requirements

- Python 3.11 or newer
- Ollama
- The `phi3:mini` Ollama model
- Packages listed in `requirements.txt`

Install the Python dependencies and model:

```bash
pip install -r requirements.txt
ollama pull phi3:mini
```

Make sure the Ollama service is running before starting the agent.

## Run

The application entry point is `main.py`:

```bash
python main.py
```

The current entry point runs one example request. A popup interface and global hotkey workflow are not implemented yet.

## Project Structure

| File | Purpose |
| --- | --- |
| `main.py` | Calls Ollama, parses the JSON response, and orchestrates tool execution. |
| `plugin_registry.py` | Registers plugin methods, describes available tools, and dispatches calls. |
| `plugin_loaded.py` | Creates the default application registry. |
| `plugins/local_files.py` | Implements the read-only local filesystem plugin. |
| `plugins/github.py` | Reserved for a future GitHub plugin. |
| `PLUGIN_ARCHITECTURE.md` | Documents the plugin boundary and authentication constraint. |
| `listener.py` | Earlier experimental tool-routing code; not used by `main.py`. |
| `ship-it.sh` | Stages, commits, and pushes Git changes; it is not the application launcher. |

## Adding a Plugin

Create a platform class under `plugins/`, keep authentication out of the class, and register its public methods in `create_default_registry()`:

```python
from plugins.example import ExamplePlatform

registry.register(
	ExamplePlatform(),
	{
		"example_action": "Description shown to the language model.",
	},
)
```

The registered method must accept keyword arguments matching the JSON `parameters` object returned by Ollama.

## Safety Notes

The default plugin only searches, inspects, and reads files. It does not delete or modify files. The agent can still expose sensitive file contents to the local model, so review plugin permissions before registering new actions.

## Development Status

This repository contains the backend and plugin foundation. The following are not currently implemented:

- Popup or desktop GUI
- Global hotkey listener
- GitHub, email, or Discord integrations
- Multi-turn conversation state
- Automated test suite
