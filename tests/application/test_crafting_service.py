import uuid
from unittest.mock import Mock

import pytest

from decker_pygame.application.crafting_service import (
    CraftingError,
    CraftingService,
    InsufficientResourcesError,
    SchematicNotFoundError,
)
from decker_pygame.application.event_dispatcher import EventDispatcher
from decker_pygame.domain.character import Character
from decker_pygame.domain.crafting import RequiredResource, Schematic
from decker_pygame.domain.ids import CharacterId
from decker_pygame.ports.repository_interfaces import CharacterRepositoryInterface


@pytest.fixture
def mock_character_repo() -> Mock:
    """Provides a mock CharacterRepository."""
    return Mock(spec=CharacterRepositoryInterface)


@pytest.fixture
def mock_event_dispatcher() -> Mock:
    """Provides a mock EventDispatcher."""
    return Mock(spec=EventDispatcher)


@pytest.fixture
def crafting_service(
    mock_character_repo: Mock, mock_event_dispatcher: Mock
) -> CraftingService:
    """Provides a CraftingService instance with mocked dependencies."""
    return CraftingService(
        character_repo=mock_character_repo, event_dispatcher=mock_event_dispatcher
    )


def test_craft_item_success(
    crafting_service: CraftingService,
    mock_character_repo: Mock,
    mock_event_dispatcher: Mock,
):
    """Tests the successful orchestration of the craft item use case."""
    # Arrange
    char_id = CharacterId(uuid.uuid4())
    schematic = Schematic(
        name="IcePick",
        produces_item_name="IcePick v1",
        produces_item_size=10,
        cost=[RequiredResource(name="credits", quantity=100)],
    )

    mock_character = Mock(autospec=Character)
    mock_character.id = char_id
    mock_character.schematics = [schematic]
    mock_character.events = [Mock()]  # Simulate an event was created
    mock_character_repo.get.return_value = mock_character

    # Act
    crafting_service.craft_item(char_id, "IcePick")

    # Assert
    mock_character_repo.get.assert_called_once_with(char_id)
    mock_character.craft.assert_called_once_with(schematic)
    mock_character_repo.save.assert_called_once_with(mock_character)
    mock_event_dispatcher.dispatch.assert_called_once_with(mock_character.events)
    mock_character.clear_events.assert_called_once()


def test_get_character_schematics(
    crafting_service: CraftingService, mock_character_repo: Mock
):
    """Tests that the service can retrieve a character's schematics."""
    # Arrange
    char_id = CharacterId(uuid.uuid4())
    schematic = Schematic("Test", "Test Item", 10, [])
    mock_character = Mock(autospec=Character)
    mock_character.schematics = [schematic]
    mock_character_repo.get.return_value = mock_character

    # Act
    result = crafting_service.get_character_schematics(char_id)

    # Assert
    mock_character_repo.get.assert_called_once_with(char_id)
    assert result == [schematic]


def test_get_schematics_for_non_existent_character(
    crafting_service: CraftingService, mock_character_repo: Mock
):
    """Tests getting schematics for a non-existent character returns an empty list."""
    char_id = CharacterId(uuid.uuid4())
    mock_character_repo.get.return_value = None

    result = crafting_service.get_character_schematics(char_id)

    assert result == []


def test_craft_item_character_not_found(
    crafting_service: CraftingService, mock_character_repo: Mock
):
    """Tests that an error is raised if the character does not exist."""
    char_id = CharacterId(uuid.uuid4())
    mock_character_repo.get.return_value = None

    with pytest.raises(CraftingError, match="not found"):
        crafting_service.craft_item(char_id, "any_schematic")


def test_craft_item_schematic_not_found(
    crafting_service: CraftingService, mock_character_repo: Mock
):
    """Tests that an error is raised if the character doesn't know the schematic."""
    char_id = CharacterId(uuid.uuid4())
    mock_character = Mock(autospec=Character)
    mock_character.schematics = []  # Empty list of schematics
    mock_character_repo.get.return_value = mock_character

    with pytest.raises(SchematicNotFoundError, match="does not know schematic"):
        crafting_service.craft_item(char_id, "Unknown Schematic")


def test_craft_item_insufficient_credits_in_domain(
    crafting_service: CraftingService, mock_character_repo: Mock
):
    """Tests that the service correctly propagates a failure from the domain layer."""
    char_id = CharacterId(uuid.uuid4())
    schematic = Schematic(
        "IcePick", "IcePick v1", 10, [RequiredResource("credits", 100)]
    )
    mock_character = Mock(autospec=Character)
    mock_character.schematics = [schematic]
    mock_character.craft.side_effect = ValueError("Insufficient credits")
    mock_character_repo.get.return_value = mock_character

    with pytest.raises(InsufficientResourcesError, match="Insufficient credits"):
        crafting_service.craft_item(char_id, "IcePick")
