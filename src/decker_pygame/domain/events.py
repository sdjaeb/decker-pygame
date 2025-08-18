"""This module defines the domain events for the application."""

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Protocol

from decker_pygame.domain.ids import CharacterId, PlayerId, ProgramId


class Event(Protocol):
    """A protocol that all domain events must adhere to."""

    @property
    def event_id(self) -> uuid.UUID:
        """The unique identifier of the event."""
        ...  # pragma: no cover

    @property
    def timestamp(self) -> datetime:
        """The UTC timestamp when the event was created."""
        ...  # pragma: no cover


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


@dataclass(frozen=True)
class ItemCrafted(BaseEvent):
    """Fired when a character successfully crafts an item."""

    character_id: CharacterId
    schematic_name: str
    item_id: ProgramId  # Could be a generic ItemId in the future
    item_name: str


@dataclass(frozen=True)
class SkillIncreased(BaseEvent):
    """Fired when a character's skill is increased."""

    character_id: CharacterId
    skill_name: str
    new_level: int


@dataclass(frozen=True)
class SkillDecreased(BaseEvent):
    """Fired when a character's skill is decreased."""

    character_id: CharacterId
    skill_name: str
    new_level: int


@dataclass(frozen=True)
class MatrixLogEntryCreated(BaseEvent):
    """Event raised when a new log entry should be displayed in the matrix view."""

    message: str
