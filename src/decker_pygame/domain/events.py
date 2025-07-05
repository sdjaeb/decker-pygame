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


@dataclass(frozen=True, kw_only=True)
class BaseEvent:
    """A base class for domain events, providing common fields."""

    event_id: uuid.UUID = field(default_factory=uuid.uuid4)
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True)
class PlayerCreated(BaseEvent):
    """Fired when a new player is created."""

    player_id: PlayerId
    name: str
    initial_health: int


@dataclass(frozen=True)
class CharacterCreated(BaseEvent):
    """Fired when a new character is created."""

    character_id: CharacterId
    name: str
