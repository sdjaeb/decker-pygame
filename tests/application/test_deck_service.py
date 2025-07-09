import uuid
from unittest.mock import Mock

import pytest

from decker_pygame.application.deck_service import (
    DeckProgramDTO,
    DeckService,
    DeckServiceError,
    DeckViewData,
)
from decker_pygame.domain.deck import Deck
from decker_pygame.domain.ids import DeckId, ProgramId
from decker_pygame.domain.program import Program
from decker_pygame.ports.repository_interfaces import DeckRepositoryInterface


def test_create_deck():
    """Tests that a new deck is created, saved, and its ID is returned."""
    mock_repo = Mock(spec=DeckRepositoryInterface)
    service = DeckService(deck_repo=mock_repo, event_dispatcher=Mock())

    deck_id = service.create_deck()

    assert isinstance(deck_id, uuid.UUID)
    mock_repo.save.assert_called_once()


def test_get_deck_view_data_success():
    """Tests successfully aggregating data for the deck view."""
    mock_repo = Mock(spec=DeckRepositoryInterface)
    service = DeckService(deck_repo=mock_repo, event_dispatcher=Mock())
    deck_id = DeckId(uuid.uuid4())

    # Configure mock deck with programs
    mock_deck = Mock(spec=Deck)
    mock_deck.programs = [
        Program(id=ProgramId(uuid.uuid4()), name="IcePick", size=10),
        Program(id=ProgramId(uuid.uuid4()), name="Hammer", size=20),
    ]
    mock_repo.get.return_value = mock_deck

    view_data = service.get_deck_view_data(deck_id)

    assert isinstance(view_data, DeckViewData)
    assert len(view_data.programs) == 2
    assert isinstance(view_data.programs[0], DeckProgramDTO)
    assert view_data.programs[0].name == "IcePick"
    assert view_data.used_deck_size == 30


def test_get_deck_view_data_not_found():
    """Tests that get_deck_view_data returns None if the deck is not found."""
    mock_repo = Mock(spec=DeckRepositoryInterface)
    service = DeckService(deck_repo=mock_repo, event_dispatcher=Mock())
    mock_repo.get.return_value = None
    assert service.get_deck_view_data(DeckId(uuid.uuid4())) is None


def test_move_program_up():
    """Tests the service method for moving a program up."""
    mock_repo = Mock(spec=DeckRepositoryInterface)
    service = DeckService(deck_repo=mock_repo, event_dispatcher=Mock())
    deck_id = DeckId(uuid.uuid4())
    mock_deck = Mock(spec=Deck)
    mock_repo.get.return_value = mock_deck

    service.move_program_up(deck_id, "TestProgram")

    mock_repo.get.assert_called_once_with(deck_id)
    mock_deck.move_program_up.assert_called_once_with("TestProgram")
    mock_repo.save.assert_called_once_with(mock_deck)


def test_move_program_down():
    """Tests the service method for moving a program down."""
    mock_repo = Mock(spec=DeckRepositoryInterface)
    service = DeckService(deck_repo=mock_repo, event_dispatcher=Mock())
    deck_id = DeckId(uuid.uuid4())
    mock_deck = Mock(spec=Deck)
    mock_repo.get.return_value = mock_deck

    service.move_program_down(deck_id, "TestProgram")

    mock_repo.get.assert_called_once_with(deck_id)
    mock_deck.move_program_down.assert_called_once_with("TestProgram")
    mock_repo.save.assert_called_once_with(mock_deck)


def test_move_program_deck_not_found():
    """Tests that moving a program fails if the deck is not found."""
    mock_repo = Mock(spec=DeckRepositoryInterface)
    service = DeckService(deck_repo=mock_repo, event_dispatcher=Mock())
    deck_id = DeckId(uuid.uuid4())
    mock_repo.get.return_value = None

    with pytest.raises(DeckServiceError, match="not found"):
        service.move_program_up(deck_id, "any")

    with pytest.raises(DeckServiceError, match="not found"):
        service.move_program_down(deck_id, "any")


def test_move_program_domain_error():
    """Tests that a domain error is correctly translated into a service error."""
    mock_repo = Mock(spec=DeckRepositoryInterface)
    service = DeckService(deck_repo=mock_repo, event_dispatcher=Mock())
    deck_id = DeckId(uuid.uuid4())
    mock_deck = Mock(spec=Deck)
    mock_repo.get.return_value = mock_deck

    # Configure the domain method to raise a ValueError
    mock_deck.move_program_up.side_effect = ValueError("Domain Error")

    with pytest.raises(DeckServiceError, match="Domain Error"):
        service.move_program_up(deck_id, "any")
