import uuid
from unittest.mock import Mock

import pytest

from decker_pygame.application.character_service import (
    CharacterDataDTO,
    CharacterService,
    CharacterServiceError,
    CharacterViewData,
)
from decker_pygame.application.player_service import PlayerStatusDTO
from decker_pygame.domain.character import Character
from decker_pygame.domain.ids import CharacterId, PlayerId
from decker_pygame.ports.repository_interfaces import CharacterRepositoryInterface
from decker_pygame.ports.service_interfaces import PlayerServiceInterface


def test_get_character_name_success():
    """Tests successfully retrieving a character's name."""
    mock_repo = Mock(spec=CharacterRepositoryInterface)
    mock_dispatcher = Mock()
    char_id = CharacterId(uuid.uuid4())
    mock_character = Mock(spec=Character)
    mock_character.name = "Testy"
    mock_repo.get.return_value = mock_character

    service = CharacterService(
        character_repo=mock_repo,
        player_service=Mock(spec=PlayerServiceInterface),
        event_dispatcher=mock_dispatcher,
    )
    name = service.get_character_name(char_id)

    mock_repo.get.assert_called_once_with(char_id)
    assert name == "Testy"


def test_get_character_name_not_found():
    """Tests retrieving a name for a character that does not exist."""
    mock_repo = Mock(spec=CharacterRepositoryInterface)
    mock_dispatcher = Mock()
    char_id = CharacterId(uuid.uuid4())
    mock_repo.get.return_value = None

    service = CharacterService(
        character_repo=mock_repo,
        player_service=Mock(spec=PlayerServiceInterface),
        event_dispatcher=mock_dispatcher,
    )
    name = service.get_character_name(char_id)

    mock_repo.get.assert_called_once_with(char_id)
    assert name is None


def test_get_character_data_success():
    """Tests successfully retrieving a character's data as a DTO."""
    mock_repo = Mock(spec=CharacterRepositoryInterface)
    mock_dispatcher = Mock()
    char_id = CharacterId(uuid.uuid4())
    mock_character = Mock(spec=Character)
    mock_character.name = "Testy"
    mock_character.credits = 1234
    mock_character.skills = {"hacking": 5}
    mock_character.unused_skill_points = 10
    # For now, reputation is not on the domain model, so the DTO default is used
    mock_repo.get.return_value = mock_character

    service = CharacterService(
        character_repo=mock_repo,
        player_service=Mock(spec=PlayerServiceInterface),
        event_dispatcher=mock_dispatcher,
    )
    dto = service.get_character_data(char_id)

    mock_repo.get.assert_called_once_with(char_id)
    assert isinstance(dto, CharacterDataDTO)
    assert dto.name == "Testy"
    assert dto.credits == 1234
    assert dto.skills == {"hacking": 5}
    assert dto.unused_skill_points == 10
    assert dto.reputation == 0  # Using default for now


def test_get_character_data_not_found():
    """Tests retrieving data for a character that does not exist."""
    mock_dispatcher = Mock()
    mock_repo = Mock(spec=CharacterRepositoryInterface)
    char_id = CharacterId(uuid.uuid4())
    mock_repo.get.return_value = None

    service = CharacterService(
        character_repo=mock_repo,
        player_service=Mock(spec=PlayerServiceInterface),
        event_dispatcher=mock_dispatcher,
    )
    dto = service.get_character_data(char_id)

    mock_repo.get.assert_called_once_with(char_id)
    assert dto is None


@pytest.fixture
def service_with_mock_char() -> tuple[
    CharacterService, Mock, Mock, Mock, Mock, CharacterId
]:
    """Provides a service with a mocked character and dependencies."""
    mock_repo = Mock(spec=CharacterRepositoryInterface)
    mock_player_service = Mock(spec=PlayerServiceInterface)
    mock_dispatcher = Mock()
    char_id = CharacterId(uuid.uuid4())
    mock_character = Mock(spec=Character)
    mock_character.events = []
    mock_repo.get.return_value = mock_character

    service = CharacterService(
        character_repo=mock_repo,
        player_service=mock_player_service,
        event_dispatcher=mock_dispatcher,
    )
    return (
        service,
        mock_character,
        mock_dispatcher,
        mock_repo,
        mock_player_service,
        char_id,
    )


def test_get_character_view_data_success(
    service_with_mock_char: tuple[
        CharacterService, Mock, Mock, Mock, Mock, CharacterId
    ],
):
    """Tests successfully aggregating data for the character view."""
    service, _, _, _, mock_player_service, char_id = service_with_mock_char
    dummy_player_id = PlayerId(uuid.uuid4())

    # Configure mocks to return valid DTOs
    service.get_character_data = Mock(
        return_value=CharacterDataDTO(
            name="Testy", credits=100, skills={"a": 1}, unused_skill_points=2
        )
    )
    mock_player_service.get_player_status.return_value = PlayerStatusDTO(
        current_health=88, max_health=100
    )

    view_data = service.get_character_view_data(char_id, dummy_player_id)

    assert isinstance(view_data, CharacterViewData)
    assert view_data.name == "Testy"
    assert view_data.health == 88
    assert view_data.credits == 100


def test_get_character_view_data_failure(
    service_with_mock_char: tuple[
        CharacterService, Mock, Mock, Mock, Mock, CharacterId
    ],
):
    """Tests that None is returned if any underlying service fails."""
    service, _, _, _, mock_player_service, char_id = service_with_mock_char
    dummy_player_id = PlayerId(uuid.uuid4())

    # Case 1: Player service fails
    service.get_character_data = Mock(return_value=Mock(spec=CharacterDataDTO))
    mock_player_service.get_player_status.return_value = None
    assert service.get_character_view_data(char_id, dummy_player_id) is None

    # Case 2: Character service fails
    service.get_character_data = Mock(return_value=None)
    mock_player_service.get_player_status.return_value = Mock(spec=PlayerStatusDTO)
    assert service.get_character_view_data(char_id, dummy_player_id) is None


def test_increase_skill_service_success(
    service_with_mock_char: tuple[
        CharacterService, Mock, Mock, Mock, Mock, CharacterId
    ],
):
    """Tests the increase_skill use case successfully orchestrates the domain."""
    service, mock_character, mock_dispatcher, mock_repo, _, char_id = (
        service_with_mock_char
    )

    service.increase_skill(char_id, "hacking")

    mock_character.increase_skill.assert_called_once_with("hacking")
    mock_repo.save.assert_called_once_with(mock_character)
    mock_dispatcher.dispatch.assert_called_once_with(mock_character.events)
    mock_character.clear_events.assert_called_once()


def test_increase_skill_service_failure(
    service_with_mock_char: tuple[
        CharacterService, Mock, Mock, Mock, Mock, CharacterId
    ],
):
    """Tests that the service translates a domain error into a service error."""
    service, mock_character, _, _, _, char_id = service_with_mock_char
    mock_character.increase_skill.side_effect = ValueError("Domain Error")

    with pytest.raises(CharacterServiceError, match="Domain Error"):
        service.increase_skill(char_id, "hacking")


def test_decrease_skill_service_success(
    service_with_mock_char: tuple[
        CharacterService, Mock, Mock, Mock, Mock, CharacterId
    ],
):
    """Tests the decrease_skill use case successfully orchestrates the domain."""
    service, mock_character, mock_dispatcher, mock_repo, _, char_id = (
        service_with_mock_char
    )

    service.decrease_skill(char_id, "hacking")

    mock_character.decrease_skill.assert_called_once_with("hacking")
    mock_repo.save.assert_called_once_with(mock_character)
    mock_dispatcher.dispatch.assert_called_once_with(mock_character.events)
    mock_character.clear_events.assert_called_once()


def test_decrease_skill_service_failure(
    service_with_mock_char: tuple[
        CharacterService, Mock, Mock, Mock, Mock, CharacterId
    ],
):
    """Tests that the service translates a domain error into a service error."""
    service, mock_character, _, _, _, char_id = service_with_mock_char
    mock_character.decrease_skill.side_effect = ValueError("Domain Error")

    with pytest.raises(CharacterServiceError, match="Domain Error"):
        service.decrease_skill(char_id, "hacking")


def test_skill_change_nonexistent_character(
    service_with_mock_char: tuple[
        CharacterService, Mock, Mock, Mock, Mock, CharacterId
    ],
):
    """Tests that skill change methods raise an error for a non-existent character."""
    service, _, _, mock_repo, _, char_id = service_with_mock_char
    mock_repo.get.return_value = None

    with pytest.raises(CharacterServiceError, match="not found"):
        service.increase_skill(char_id, "hacking")

    with pytest.raises(CharacterServiceError, match="not found"):
        service.decrease_skill(char_id, "hacking")
