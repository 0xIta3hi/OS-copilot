"""Read-only local file system plugin."""

from pathlib import Path


class LocalFileSystem:
    """Expose safe file-system actions to the agent."""

    def __init__(self, root: str | Path | None = None, max_results: int = 50):
        self.root = Path(root or Path.home()).expanduser().resolve()
        self.max_results = max_results

    def _resolve(self, path: str | Path) -> Path:
        candidate = (self.root / path).expanduser().resolve()
        try:
            candidate.relative_to(self.root)
        except ValueError as error:
            raise ValueError("Path must stay inside the plugin root") from error
        return candidate

    def file_search(self, keyword: str, path: str | Path = ".") -> list[str]:
        """Return up to ``max_results`` files whose names contain ``keyword``."""
        search_root = self._resolve(path)
        if not search_root.is_dir():
            raise NotADirectoryError(f"Search path is not a directory: {search_root}")

        keyword = keyword.casefold()
        matches = (
            item
            for item in search_root.rglob("*")
            if item.is_file() and keyword in item.name.casefold()
        )
        return [str(item) for item in sorted(matches)[: self.max_results]]

    def file_system_manipulation(self, action: str, path: str | Path = ".") -> dict:
        """Inspect a path without modifying the file system."""
        target = self._resolve(path)
        if action == "exists":
            return {"path": str(target), "exists": target.exists()}
        if action == "list":
            if not target.is_dir():
                raise NotADirectoryError(f"Path is not a directory: {target}")
            return {
                "path": str(target),
                "entries": sorted(item.name for item in target.iterdir()),
            }
        if action == "info":
            if not target.exists():
                return {"path": str(target), "exists": False}
            return {
                "path": str(target),
                "exists": True,
                "is_file": target.is_file(),
                "is_directory": target.is_dir(),
                "size": target.stat().st_size if target.is_file() else None,
            }
        raise ValueError("Unsupported action. Use 'exists', 'list', or 'info'.")

    def open_file(self, filename: str | Path, path: str | Path = ".") -> str:
        """Read a UTF-8 text file below the plugin root."""
        target = self._resolve(Path(path) / filename)
        if not target.is_file():
            raise FileNotFoundError(f"File not found: {target}")
        return target.read_text(encoding="utf-8")


# Keep the original name available while callers migrate to the standard form.
Local_File_system = LocalFileSystem

