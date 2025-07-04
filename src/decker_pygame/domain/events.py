import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Protocol

from decker_pygame.domain.ids import CharacterId, PlayerId


class Event(Protocol):
    """A protocol that all domain events must adhere to."""

    @property
    def event_id(self) -> uuid.UUID: ...

    @property
    def timestamp(self) -> datetime: ...


@dataclass(frozen=True)
class PlayerCreated:
    """Fired when a new player is created."""

    # Event-specific fields come first
    player_id: PlayerId
    name: str
    initial_health: int

    # Common event fields come last, with defaults
    event_id: uuid.UUID = field(default_factory=uuid.uuid4)
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True)
class CharacterCreated:
    """Fired when a new character is created."""

    character_id: CharacterId
    name: str

    event_id: uuid.UUID = field(default_factory=uuid.uuid4)
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
