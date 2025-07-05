import json
from typing import Any, Protocol


class LogWriter(Protocol):
    """A protocol for log writing strategies."""

    def write(self, message: str, data: dict[str, Any]) -> None:
        """Writes a log entry."""
        ...  # pragma: no cover


class ConsoleLogWriter:
    """A LogWriter that prints formatted JSON to the console."""

    def write(self, message: str, data: dict[str, Any]) -> None:
        log_entry = {"message": message, "data": data}
        print(f"LOG: {json.dumps(log_entry, indent=2)}")


class LoggingService:
    """A service for dispatching log messages to various writers."""

    def __init__(self, writers: list[LogWriter] | None = None) -> None:
        self._writers = writers or []

    def register(self, writer: LogWriter) -> None:
        """Register a new log writer."""
        self._writers.append(writer)

    def log(self, message: str, data: dict[str, Any]) -> None:
        """Send a log message to all registered writers."""
        for writer in self._writers:
            writer.write(message, data)
