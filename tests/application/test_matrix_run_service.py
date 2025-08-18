"""Tests for the MatrixRunService."""

import uuid
from unittest.mock import Mock

import pytest

from decker_pygame.application.matrix_run_service import MatrixRunService
from decker_pygame.domain.character import Character
from decker_pygame.domain.deck import Deck, Program
from decker_pygame.domain.events import MatrixLogEntryCreated
from decker_pygame.domain.ids import (
    CharacterId,
    DeckId,
    NodeId,
    PlayerId,
    ProgramId,
)
from decker_pygame.domain.player import Player
from decker_pygame.domain.system import Node, System


@pytest.fixture
def mock_repos() -> dict[str, Mock]:
    """Provides mock repositories."""
    return {
        "character_repo": Mock(),
        "deck_repo": Mock(),
        "player_repo": Mock(),
        "system_repo": Mock(),
    }


def test_get_matrix_run_view_data(mock_repos: dict[str, Mock]):
    """Tests that the service correctly fetches data and creates a DTO."""
    # Arrange
    player_id = PlayerId(uuid.uuid4())
    character_id = CharacterId(uuid.uuid4())
    deck_id = DeckId(uuid.uuid4())

    mock_player = Mock(spec=Player)
    mock_player.health = 80

    mock_deck = Mock(spec=Deck)
    mock_deck.health = 90
    mock_deck.programs = [
        Program(id=ProgramId(uuid.uuid4()), name="TestProgram", size=10)
    ]

    mock_character = Mock(spec=Character)
    mock_character.deck_id = deck_id

    cpu_node = Node(id=NodeId(uuid.uuid4()), name="CPU", position=(50, 50))
    data_node = Node(id=NodeId(uuid.uuid4()), name="Data Store 1", position=(100, 100))
    mock_system = Mock(spec=System)
    mock_system.nodes = [cpu_node, data_node]
    mock_system.connections = [(cpu_node.id, data_node.id)]

    mock_repos["player_repo"].get.return_value = mock_player
    mock_repos["deck_repo"].get.return_value = mock_deck
    mock_repos["character_repo"].get.return_value = mock_character
    mock_repos["system_repo"].get.return_value = mock_system

    service = MatrixRunService(**mock_repos)
    service._messages = ["Test Message"]  # Manually set for test

    # Act
    dto = service.get_matrix_run_view_data(character_id, player_id)

    # Assert
    assert dto.physical_health == 80.0
    assert dto.deck_health == 90.0
    assert dto.software == ["TestProgram"]
    assert dto.nodes == {"CPU": (50, 50), "Data Store 1": (100, 100)}
    assert dto.connections == [("CPU", "Data Store 1")]
    assert dto.messages == ["Test Message"]


def test_get_matrix_run_view_data_with_missing_aggregates(mock_repos: dict[str, Mock]):
    """Tests that the service returns a default DTO if an aggregate is missing."""
    mock_repos["character_repo"].get.return_value = None
    mock_repos["system_repo"].get.return_value = None
    service = MatrixRunService(**mock_repos)
    dto = service.get_matrix_run_view_data(
        CharacterId(uuid.uuid4()), PlayerId(uuid.uuid4())
    )
    assert dto.physical_health == 100.0


def test_on_matrix_log_entry(mock_repos: dict[str, Mock]):
    """Tests that the service correctly handles and stores matrix log events."""
    # Arrange
    service = MatrixRunService(**mock_repos)
    event1 = MatrixLogEntryCreated(message="Message 1")
    event2 = MatrixLogEntryCreated(message="Message 2")

    # Act
    service.on_matrix_log_entry(event1)
    service.on_matrix_log_entry(event2)

    # Assert
    assert service._messages == ["Message 1", "Message 2"]


def test_on_matrix_log_entry_respects_max_messages(mock_repos: dict[str, Mock]):
    """Tests that the message list is trimmed to the max size."""
    # Arrange
    service = MatrixRunService(**mock_repos)
    service._max_messages = 2

    service.on_matrix_log_entry(MatrixLogEntryCreated(message="A"))
    service.on_matrix_log_entry(MatrixLogEntryCreated(message="B"))
    service.on_matrix_log_entry(MatrixLogEntryCreated(message="C"))

    assert service._messages == ["B", "C"]
