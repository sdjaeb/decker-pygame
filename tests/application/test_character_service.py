import uuid
from unittest.mock import Mock

import pytest

from decker_pygame.application.character_service import (
    CharacterDataDTO,
    CharacterService,
    CharacterServiceError,
)
from decker_pygame.domain.character import Character
from decker_pygame.domain.character_repository_interface import (
    CharacterRepositoryInterface,
)
from decker_pygame.domain.ids import CharacterId


def test_get_character_name_success():
    """Tests successfully retrieving a character's name."""
    mock_repo = Mock(spec=CharacterRepositoryInterface)
    mock_dispatcher = Mock()
    char_id = CharacterId(uuid.uuid4())
    mock_character = Mock(spec=Character)
    mock_character.name = "Testy"
    mock_repo.get.return_value = mock_character

    service = CharacterService(
        character_repo=mock_repo, event_dispatcher=mock_dispatcher
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
        character_repo=mock_repo, event_dispatcher=mock_dispatcher
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
        character_repo=mock_repo, event_dispatcher=mock_dispatcher
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
        character_repo=mock_repo, event_dispatcher=mock_dispatcher
    )
    dto = service.get_character_data(char_id)

    mock_repo.get.assert_called_once_with(char_id)
    assert dto is None


@pytest.fixture
def service_with_mock_char() -> tuple[CharacterService, Mock, Mock, Mock, CharacterId]:
    """Provides a service with a mocked character and dependencies."""
    mock_repo = Mock(spec=CharacterRepositoryInterface)
    mock_dispatcher = Mock()
    char_id = CharacterId(uuid.uuid4())
    mock_character = Mock(spec=Character)
    mock_character.events = []
    mock_repo.get.return_value = mock_character

    service = CharacterService(
        character_repo=mock_repo, event_dispatcher=mock_dispatcher
    )
    return service, mock_character, mock_dispatcher, mock_repo, char_id


def test_increase_skill_service_success(
    service_with_mock_char: tuple[CharacterService, Mock, Mock, Mock, CharacterId],
):
    """Tests the increase_skill use case successfully orchestrates the domain."""
    service, mock_character, mock_dispatcher, mock_repo, char_id = (
        service_with_mock_char
    )

    service.increase_skill(char_id, "hacking")

    mock_character.increase_skill.assert_called_once_with("hacking")
    mock_repo.save.assert_called_once_with(mock_character)
    mock_dispatcher.dispatch.assert_called_once_with(mock_character.events)
    mock_character.clear_events.assert_called_once()


def test_increase_skill_service_failure(
    service_with_mock_char: tuple[CharacterService, Mock, Mock, Mock, CharacterId],
):
    """Tests that the service translates a domain error into a service error."""
    service, mock_character, _, _, char_id = service_with_mock_char
    mock_character.increase_skill.side_effect = ValueError("Domain Error")

    with pytest.raises(CharacterServiceError, match="Domain Error"):
        service.increase_skill(char_id, "hacking")


def test_decrease_skill_service_success(
    service_with_mock_char: tuple[CharacterService, Mock, Mock, Mock, CharacterId],
):
    """Tests the decrease_skill use case successfully orchestrates the domain."""
    service, mock_character, mock_dispatcher, mock_repo, char_id = (
        service_with_mock_char
    )

    service.decrease_skill(char_id, "hacking")

    mock_character.decrease_skill.assert_called_once_with("hacking")
    mock_repo.save.assert_called_once_with(mock_character)
    mock_dispatcher.dispatch.assert_called_once_with(mock_character.events)
    mock_character.clear_events.assert_called_once()


def test_decrease_skill_service_failure(
    service_with_mock_char: tuple[CharacterService, Mock, Mock, Mock, CharacterId],
):
    """Tests that the service translates a domain error into a service error."""
    service, mock_character, _, _, char_id = service_with_mock_char
    mock_character.decrease_skill.side_effect = ValueError("Domain Error")

    with pytest.raises(CharacterServiceError, match="Domain Error"):
        service.decrease_skill(char_id, "hacking")


def test_skill_change_nonexistent_character(
    service_with_mock_char: tuple[CharacterService, Mock, Mock, Mock, CharacterId],
):
    """Tests that skill change methods raise an error for a non-existent character."""
    service, _, _, mock_repo, char_id = service_with_mock_char
    mock_repo.get.return_value = None

    with pytest.raises(CharacterServiceError, match="not found"):
        service.increase_skill(char_id, "hacking")

    with pytest.raises(CharacterServiceError, match="not found"):
        service.decrease_skill(char_id, "hacking")
