"""Tests for the MatrixRunService."""

import uuid
from unittest.mock import Mock

import pytest

from decker_pygame.application.matrix_run_service import MatrixRunService
from decker_pygame.domain.character import Character
from decker_pygame.domain.deck import Deck, Program
from decker_pygame.domain.ids import CharacterId, DeckId, PlayerId, ProgramId
from decker_pygame.domain.player import Player


@pytest.fixture
def mock_repos() -> dict[str, Mock]:
    """Provides mock repositories."""
    return {
        "character_repo": Mock(),
        "deck_repo": Mock(),
        "player_repo": Mock(),
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

    mock_repos["player_repo"].get.return_value = mock_player
    mock_repos["deck_repo"].get.return_value = mock_deck
    mock_repos["character_repo"].get.return_value = mock_character

    service = MatrixRunService(**mock_repos)

    # Act
    dto = service.get_matrix_run_view_data(character_id, player_id)

    # Assert
    assert dto.physical_health == 80.0
    assert dto.deck_health == 90.0
    assert dto.software == ["TestProgram"]


def test_get_matrix_run_view_data_with_missing_aggregates(mock_repos: dict[str, Mock]):
    """Tests that the service returns a default DTO if an aggregate is missing."""
    mock_repos["character_repo"].get.return_value = None
    service = MatrixRunService(**mock_repos)
    dto = service.get_matrix_run_view_data(
        CharacterId(uuid.uuid4()), PlayerId(uuid.uuid4())
    )
    assert dto.physical_health == 100.0
