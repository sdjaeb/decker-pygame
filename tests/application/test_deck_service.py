import uuid
from unittest.mock import Mock

from decker_pygame.application.deck_service import (
    DeckProgramDTO,
    DeckService,
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
    # Use real domain objects for simple data containers instead of mocks
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
