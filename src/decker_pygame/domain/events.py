import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Protocol


class Event(Protocol):
    """A protocol that all domain events must adhere to."""

    event_id: uuid.UUID
    timestamp: datetime


@dataclass(frozen=True)
class PlayerCreated:
    """Fired when a new player is created."""

    # Event-specific fields come first
    player_id: uuid.UUID
    name: str
    initial_health: int

    # Common event fields come last, with defaults
    event_id: uuid.UUID = field(default_factory=uuid.uuid4)
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
