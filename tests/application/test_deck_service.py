import uuid
from unittest.mock import Mock

import pytest

from decker_pygame.application.deck_service import (
    DeckProgramDTO,
    DeckService,
    DeckServiceError,
    DeckViewData,
    TransferViewData,
)
from decker_pygame.application.event_dispatcher import EventDispatcher
from decker_pygame.domain.character import Character
from decker_pygame.domain.deck import Deck
from decker_pygame.domain.ids import CharacterId, DeckId, ProgramId
from decker_pygame.domain.program import Program
from decker_pygame.ports.repository_interfaces import (
    CharacterRepositoryInterface,
    DeckRepositoryInterface,
)


@pytest.fixture
def mock_deck_repo() -> Mock:
    """Provides a mock DeckRepository."""
    return Mock(spec=DeckRepositoryInterface)


@pytest.fixture
def mock_char_repo() -> Mock:
    """Provides a mock CharacterRepository."""
    return Mock(spec=CharacterRepositoryInterface)


@pytest.fixture
def mock_dispatcher() -> Mock:
    """Provides a mock EventDispatcher."""
    return Mock(spec=EventDispatcher)


@pytest.fixture
def deck_service(
    mock_deck_repo: Mock, mock_char_repo: Mock, mock_dispatcher: Mock
) -> DeckService:
    """Provides a DeckService instance with mocked dependencies."""
    return DeckService(
        deck_repo=mock_deck_repo,
        character_repo=mock_char_repo,
        event_dispatcher=mock_dispatcher,
    )


def test_create_deck(deck_service: DeckService, mock_deck_repo: Mock):
    """Tests that a new deck is created, saved, and its ID is returned."""
    deck_id = deck_service.create_deck()

    assert isinstance(deck_id, uuid.UUID)
    mock_deck_repo.save.assert_called_once()


def test_get_deck_view_data_success(deck_service: DeckService, mock_deck_repo: Mock):
    """Tests successfully aggregating data for the deck view."""
    deck_id = DeckId(uuid.uuid4())

    # Configure mock deck with programs
    mock_deck = Mock(spec=Deck)
    mock_deck.programs = [
        Program(id=ProgramId(uuid.uuid4()), name="IcePick", size=10),
        Program(id=ProgramId(uuid.uuid4()), name="Hammer", size=20),
    ]
    mock_deck_repo.get.return_value = mock_deck

    view_data = deck_service.get_deck_view_data(deck_id)

    assert isinstance(view_data, DeckViewData)
    assert len(view_data.programs) == 2
    assert isinstance(view_data.programs[0], DeckProgramDTO)
    assert view_data.programs[0].name == "IcePick"
    assert view_data.used_deck_size == 30


def test_get_deck_view_data_not_found(deck_service: DeckService, mock_deck_repo: Mock):
    """Tests that get_deck_view_data returns None if the deck is not found."""
    mock_deck_repo.get.return_value = None
    assert deck_service.get_deck_view_data(DeckId(uuid.uuid4())) is None


def test_move_program_up(deck_service: DeckService, mock_deck_repo: Mock):
    """Tests the service method for moving a program up."""
    deck_id = DeckId(uuid.uuid4())
    mock_deck = Mock(spec=Deck)
    mock_deck_repo.get.return_value = mock_deck

    deck_service.move_program_up(deck_id, "TestProgram")

    mock_deck_repo.get.assert_called_once_with(deck_id)
    mock_deck.move_program_up.assert_called_once_with("TestProgram")
    mock_deck_repo.save.assert_called_once_with(mock_deck)


def test_move_program_down(deck_service: DeckService, mock_deck_repo: Mock):
    """Tests the service method for moving a program down."""
    deck_id = DeckId(uuid.uuid4())
    mock_deck = Mock(spec=Deck)
    mock_deck_repo.get.return_value = mock_deck

    deck_service.move_program_down(deck_id, "TestProgram")

    mock_deck_repo.get.assert_called_once_with(deck_id)
    mock_deck.move_program_down.assert_called_once_with("TestProgram")
    mock_deck_repo.save.assert_called_once_with(mock_deck)


def test_move_program_deck_not_found(deck_service: DeckService, mock_deck_repo: Mock):
    """Tests that moving a program fails if the deck is not found."""
    deck_id = DeckId(uuid.uuid4())
    mock_deck_repo.get.return_value = None

    with pytest.raises(DeckServiceError, match="not found"):
        deck_service.move_program_up(deck_id, "any")

    with pytest.raises(DeckServiceError, match="not found"):
        deck_service.move_program_down(deck_id, "any")


def test_move_program_domain_error(deck_service: DeckService, mock_deck_repo: Mock):
    """Tests that a domain error is correctly translated into a service error."""
    deck_id = DeckId(uuid.uuid4())
    mock_deck = Mock(spec=Deck)
    mock_deck_repo.get.return_value = mock_deck

    # Configure the domain method to raise a ValueError
    mock_deck.move_program_up.side_effect = ValueError("Domain Error")

    with pytest.raises(DeckServiceError, match="Domain Error"):
        deck_service.move_program_up(deck_id, "any")


def test_get_transfer_view_data_success(
    deck_service: DeckService, mock_deck_repo: Mock, mock_char_repo: Mock
):
    """Tests successfully aggregating data for the transfer view."""
    char_id = CharacterId(uuid.uuid4())

    # Configure mock character and deck
    mock_character = Mock(spec=Character)
    mock_character.deck_id = DeckId(uuid.uuid4())
    mock_character.stored_programs = [
        Program(id=ProgramId(uuid.uuid4()), name="IcePick", size=10)
    ]
    mock_char_repo.get.return_value = mock_character

    mock_deck = Mock(spec=Deck)
    mock_deck.programs = [Program(id=ProgramId(uuid.uuid4()), name="Hammer", size=20)]
    mock_deck_repo.get.return_value = mock_deck

    view_data = deck_service.get_transfer_view_data(char_id)

    assert isinstance(view_data, TransferViewData)
    assert len(view_data.stored_programs) == 1
    assert view_data.stored_programs[0].name == "IcePick"
    assert len(view_data.deck_programs) == 1
    assert view_data.deck_programs[0].name == "Hammer"


def test_get_transfer_view_data_not_found(
    deck_service: DeckService, mock_deck_repo: Mock, mock_char_repo: Mock
):
    """Tests that get_transfer_view_data returns None if character or deck not found."""
    mock_char_repo.get.return_value = None
    assert deck_service.get_transfer_view_data(CharacterId(uuid.uuid4())) is None

    mock_character = Mock(spec=Character)
    mock_character.deck_id = DeckId(uuid.uuid4())
    mock_char_repo.get.return_value = mock_character
    mock_deck_repo.get.return_value = None
    assert deck_service.get_transfer_view_data(CharacterId(uuid.uuid4())) is None


def test_move_program_to_deck(
    deck_service: DeckService, mock_deck_repo: Mock, mock_char_repo: Mock
):
    """Tests moving a program from storage to the deck."""
    char_id = CharacterId(uuid.uuid4())
    program_name = "IcePick"
    program_to_move = Program(id=ProgramId(uuid.uuid4()), name=program_name, size=10)

    mock_character = Mock(spec=Character)
    mock_character.deck_id = DeckId(uuid.uuid4())
    mock_character.remove_stored_program.return_value = program_to_move
    mock_char_repo.get.return_value = mock_character

    mock_deck = Mock(spec=Deck)
    mock_deck_repo.get.return_value = mock_deck

    deck_service.move_program_to_deck(char_id, program_name)

    mock_char_repo.get.assert_called_once_with(char_id)
    mock_deck_repo.get.assert_called_once_with(mock_character.deck_id)
    mock_character.remove_stored_program.assert_called_once_with(program_name)
    mock_deck.add_program.assert_called_once_with(program_to_move)
    mock_char_repo.save.assert_called_once_with(mock_character)
    mock_deck_repo.save.assert_called_once_with(mock_deck)


def test_move_program_to_storage(
    deck_service: DeckService, mock_deck_repo: Mock, mock_char_repo: Mock
):
    """Tests moving a program from the deck to storage."""
    char_id = CharacterId(uuid.uuid4())
    program_name = "Hammer"
    program_to_move = Program(id=ProgramId(uuid.uuid4()), name=program_name, size=20)

    mock_character = Mock(spec=Character)
    mock_character.deck_id = DeckId(uuid.uuid4())
    mock_character.stored_programs = []
    mock_char_repo.get.return_value = mock_character

    mock_deck = Mock(spec=Deck)
    mock_deck.remove_program.return_value = program_to_move
    mock_deck_repo.get.return_value = mock_deck

    deck_service.move_program_to_storage(char_id, program_name)

    mock_char_repo.get.assert_called_once_with(char_id)
    mock_deck_repo.get.assert_called_once_with(mock_character.deck_id)
    mock_deck.remove_program.assert_called_once_with(program_name)
    assert mock_character.stored_programs == [program_to_move]
    mock_char_repo.save.assert_called_once_with(mock_character)
    mock_deck_repo.save.assert_called_once_with(mock_deck)


def test_move_program_transfer_fails_if_not_found(
    deck_service: DeckService, mock_deck_repo: Mock, mock_char_repo: Mock
):
    """Tests that transfer use cases raise an error if the program is not found."""
    char_id = CharacterId(uuid.uuid4())
    program_name = "Ghost"

    mock_character = Mock(spec=Character)
    mock_character.deck_id = DeckId(uuid.uuid4())
    mock_character.remove_stored_program.side_effect = ValueError("not found")
    mock_char_repo.get.return_value = mock_character

    mock_deck = Mock(spec=Deck)
    mock_deck.remove_program.side_effect = ValueError("not found")
    mock_deck_repo.get.return_value = mock_deck

    with pytest.raises(DeckServiceError, match="not found"):
        deck_service.move_program_to_deck(char_id, program_name)

    with pytest.raises(DeckServiceError, match="not found"):
        deck_service.move_program_to_storage(char_id, program_name)


def test_move_program_transfer_repo_failure(
    deck_service: DeckService, mock_deck_repo: Mock, mock_char_repo: Mock
):
    """Tests that transfer fails if character or deck is not found."""
    char_id = CharacterId(uuid.uuid4())

    # Case 1: Character not found
    mock_char_repo.get.return_value = None
    with pytest.raises(DeckServiceError, match="Character.*not found"):
        deck_service.move_program_to_deck(char_id, "any")
    with pytest.raises(DeckServiceError, match="Character.*not found"):
        deck_service.move_program_to_storage(char_id, "any")

    # Case 2: Deck not found
    mock_character = Mock(spec=Character)
    mock_character.deck_id = DeckId(uuid.uuid4())
    mock_char_repo.get.return_value = mock_character
    mock_deck_repo.get.return_value = None
    with pytest.raises(DeckServiceError, match="Deck.*not found"):
        deck_service.move_program_to_deck(char_id, "any")
    with pytest.raises(DeckServiceError, match="Deck.*not found"):
        deck_service.move_program_to_storage(char_id, "any")
