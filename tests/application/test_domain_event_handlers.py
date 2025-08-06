"""This module contains tests for the domain event handlers."""

import uuid
from dataclasses import dataclass
from unittest.mock import ANY, Mock

import pytest

from decker_pygame.application.domain_event_handlers import (
    create_event_logging_handler,
    is_special_player,
    log_special_player_created,
)
from decker_pygame.domain.events import BaseEvent, PlayerCreated
from decker_pygame.domain.ids import PlayerId


def test_create_event_logging_handler():
    """Tests that the factory creates a handler that logs events."""
    mock_logging_service = Mock()
    handler = create_event_logging_handler(mock_logging_service)

    @dataclass(frozen=True)
    class DummyEvent(BaseEvent):
        id: int = 1
        name: str = "test"

    event = DummyEvent()
    handler(event)

    mock_logging_service.log.assert_called_once_with(
        "Domain Event: DummyEvent",
        data={"id": "1", "name": "test", "event_id": ANY, "timestamp": ANY},
    )


def test_log_special_player_created(capsys):
    """Tests that the special handler prints the correct message."""
    event = PlayerCreated(
        player_id=PlayerId(uuid.uuid4()), name="Rynn", initial_health=100
    )
    log_special_player_created(event)
    captured = capsys.readouterr()
    assert "EVENT LOG: A special player named 'Rynn' was created!" in captured.out


@pytest.mark.parametrize(
    "player_name, expected",
    [("Rynn", True), ("rynn", True), ("Deckard", False)],
)
def test_is_special_player(player_name: str, expected: bool):
    """Tests the condition function for identifying the special player."""
    event = PlayerCreated(
        player_id=PlayerId(uuid.uuid4()), name=player_name, initial_health=100
    )
    assert is_special_player(event) is expected
