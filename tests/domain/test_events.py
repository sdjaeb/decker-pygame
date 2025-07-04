import uuid
from dataclasses import FrozenInstanceError
from datetime import datetime

import pytest

from decker_pygame.domain.events import CharacterCreated, PlayerCreated
from decker_pygame.domain.ids import CharacterId, PlayerId


def test_player_created_event_is_a_dataclass():
    """Verify the structure and default values of the PlayerCreated event."""
    player_id = PlayerId(uuid.uuid4())
    event = PlayerCreated(player_id=player_id, name="Deckard", initial_health=100)

    assert event.player_id == player_id
    assert event.name == "Deckard"
    assert isinstance(event.event_id, uuid.UUID)
    assert isinstance(event.timestamp, datetime)

    # Verify the event is immutable by attempting to change a field
    with pytest.raises(FrozenInstanceError):
        event.name = "New Name"  # type: ignore[attr-defined]


def test_character_created_event_is_a_dataclass():
    """Verify the structure and default values of the CharacterCreated event."""
    char_id = CharacterId(uuid.uuid4())
    event = CharacterCreated(character_id=char_id, name="Rynn")

    assert event.character_id == char_id
    assert event.name == "Rynn"
    assert isinstance(event.event_id, uuid.UUID)
    assert isinstance(event.timestamp, datetime)

    # Verify the event is immutable by attempting to change a field
    with pytest.raises(FrozenInstanceError):
        event.name = "New Name"  # type: ignore[attr-defined]
