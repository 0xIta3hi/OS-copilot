"""Plugin discovery, tool metadata, and execution."""

from dataclasses import dataclass
from typing import Any, Callable

from plugins.local_files import LocalFileSystem


@dataclass(frozen=True)
class Tool: # base class for a tool.
	name: str
	description: str
	handler: Callable[..., Any]


class PluginRegistry:
	"""Keep platform plugins isolated from the agent and authentication code."""

	def __init__(self) -> None: # adds tools to the registry and keeps track of them in a dictionary.
		self._tools: dict[str, Tool] = {}

	def register(self, plugin: object, tools: dict[str, str]) -> None: # add a tool to registry ie "registers" a tool
		for name, description in tools.items():
			handler = getattr(plugin, name) # handler : a callable function mapped to the tool_name and associated function of the tool
			self._tools[name] = Tool(name, description, handler)

	def describe(self) -> str: #describes available tools
		return "\n".join(
			f"- {tool.name}: {tool.description}" for tool in self._tools.values()
		)

	def execute(self, name: str, parameters: dict[str, Any] | None = None) -> Any: # execcutes a tool by name 
		if name not in self._tools:
			raise ValueError(f"Unknown tool: {name}")
		return self._tools[name].handler(**(parameters or {}))

	def has_tool(self, name: str) -> bool: # checks if a tool is registered or not. 
		return name in self._tools


def create_default_registry() -> PluginRegistry:
	registry = PluginRegistry() # creates a instance of plugin registry.
	registry.register( # registers tools to the registry with their descriptions and handlers, in this case the LocalFileSystem plugin with its methods.
		LocalFileSystem(),
		{
			"file_search": "Search file names below the home directory.",
			"open_file": "Read a UTF-8 text file below the home directory.",
			"file_system_manipulation": (
				"Inspect a path using the exists, list, or info action."
			),
		},
	)
	return registry

