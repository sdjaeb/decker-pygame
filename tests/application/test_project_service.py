"""This module contains tests for the ProjectService."""

import uuid
from unittest.mock import Mock, patch

import pytest

from decker_pygame.application.dtos import NewProjectViewDTO, ProjectDataViewDTO
from decker_pygame.application.project_service import ProjectError, ProjectService
from decker_pygame.domain.character import Character
from decker_pygame.domain.crafting import Schematic
from decker_pygame.domain.ids import CharacterId, DeckId
from decker_pygame.domain.project import ActiveProject
from decker_pygame.ports.repository_interfaces import CharacterRepositoryInterface


@pytest.fixture
def mock_character_repo() -> Mock:
    """Provides a mock CharacterRepository."""
    return Mock(spec=CharacterRepositoryInterface)


@pytest.fixture
def project_service(mock_character_repo: Mock) -> ProjectService:
    """Provides a ProjectService instance with a mock repository."""
    return ProjectService(mock_character_repo)


@pytest.fixture
def character() -> Character:
    """Provides a default character instance for testing."""
    return Character.create(
        character_id=CharacterId(uuid.uuid4()),
        name="Test Decker",
        deck_id=DeckId(uuid.uuid4()),
        initial_skills={"Programming": 0, "Chip Design": 0},
        initial_credits=1000,
        initial_skill_points=5,
        initial_reputation=0,
    )


def test_start_new_project_success(
    project_service: ProjectService, mock_character_repo: Mock, character: Character
):
    """Tests a project can be started successfully with correct time calculation."""
    mock_character_repo.get.return_value = character
    char_id = CharacterId(character.id)

    project_service.start_new_project(
        character_id=char_id, item_type="software", item_class="Test ICE", rating=3
    )

    mock_character_repo.get.assert_called_once_with(char_id)
    mock_character_repo.save.assert_called_once_with(character)

    project = character.active_project
    assert project is not None
    assert project.item_type == "software"
    assert project.item_class == "Test ICE"
    assert project.target_rating == 3
    # Time calculation: rating^2 * 100 = 3*3*100 = 900
    assert project.time_required == 900


def test_start_new_project_with_skill_reduction(
    project_service: ProjectService, mock_character_repo: Mock, character: Character
):
    """Tests that research time is reduced by the character's skill level."""
    character.skills["Programming"] = 5
    mock_character_repo.get.return_value = character
    char_id = CharacterId(character.id)

    project_service.start_new_project(
        character_id=char_id, item_type="software", item_class="Test ICE", rating=4
    )

    project = character.active_project
    assert project is not None
    # Time: 4*4*100 - 5*5*10 = 1600 - 250 = 1350
    assert project.time_required == 1350


def test_start_new_project_with_schematic_reduction(
    project_service: ProjectService, mock_character_repo: Mock, character: Character
):
    """Tests that research time is reduced by existing schematics."""
    character.schematics.append(Schematic("v2", "Test ICE v2", 1, 2, []))
    mock_character_repo.get.return_value = character
    char_id = CharacterId(character.id)

    project_service.start_new_project(
        character_id=char_id, item_type="software", item_class="Test ICE", rating=4
    )

    project = character.active_project
    assert project is not None
    # Time: 4*4*100 - 2*2*25 = 1600 - 100 = 1500
    assert project.time_required == 1500


def test_start_new_project_minimum_time(
    project_service: ProjectService, mock_character_repo: Mock, character: Character
):
    """Tests that research time has a minimum value."""
    character.skills["Programming"] = 10  # High skill to force time below minimum
    mock_character_repo.get.return_value = character
    char_id = CharacterId(character.id)

    project_service.start_new_project(
        character_id=char_id, item_type="software", item_class="Test ICE", rating=1
    )

    project = character.active_project
    assert project is not None
    # Time: 1*1*100 - 10*10*10 = -900. Should be capped at 10.
    assert project.time_required == 10


def test_start_new_project_character_not_found(
    project_service: ProjectService, mock_character_repo: Mock
):
    """Tests that an error is raised if the character is not found."""
    mock_character_repo.get.return_value = None
    char_id = CharacterId(uuid.uuid4())

    with pytest.raises(ProjectError, match="not found"):
        project_service.start_new_project(char_id, "software", "Test", 1)


def test_start_new_project_already_active(
    project_service: ProjectService, mock_character_repo: Mock, character: Character
):
    """Tests that an error is raised if a project is already active."""
    character.active_project = Mock()
    mock_character_repo.get.return_value = character
    char_id = CharacterId(character.id)

    with pytest.raises(ProjectError, match="already has an active project"):
        project_service.start_new_project(char_id, "software", "Test", 1)


def test_start_new_project_invalid_item_type(
    project_service: ProjectService, mock_character_repo: Mock, character: Character
):
    """Tests that an error is raised for an invalid item type."""
    mock_character_repo.get.return_value = character
    char_id = CharacterId(character.id)

    with pytest.raises(ProjectError, match="Invalid item type"):
        project_service.start_new_project(char_id, "invalid_type", "Test", 1)


def test_work_on_project_success(
    project_service: ProjectService, mock_character_repo: Mock, character: Character
):
    """Tests that time can be successfully added to a project."""
    # Setup: Character has an active project
    project = ActiveProject("software", "Test ICE", 1, 100, 25)
    character.active_project = project
    mock_character_repo.get.return_value = character
    char_id = CharacterId(character.id)

    # Act
    project_service.work_on_project(char_id, 50)

    # Assert
    mock_character_repo.get.assert_called_once_with(char_id)
    assert project.time_spent == 75
    mock_character_repo.save.assert_called_once_with(character)


def test_work_on_project_character_not_found(
    project_service: ProjectService, mock_character_repo: Mock
):
    """Tests that an error is raised if the character is not found."""
    mock_character_repo.get.return_value = None
    char_id = CharacterId(uuid.uuid4())

    with pytest.raises(ProjectError, match="not found"):
        project_service.work_on_project(char_id, 10)


def test_work_on_project_no_active_project(
    project_service: ProjectService, mock_character_repo: Mock, character: Character
):
    """Tests that an error is raised if the character has no active project."""
    # Setup: Character has NO active project
    character.active_project = None
    mock_character_repo.get.return_value = character
    char_id = CharacterId(character.id)

    with pytest.raises(ProjectError, match="no active project to work on"):
        project_service.work_on_project(char_id, 10)


def test_complete_project_success(
    project_service: ProjectService, mock_character_repo: Mock, character: Character
):
    """Tests that a completed project successfully awards a schematic on a good roll."""
    # Setup: Project is finished, character has high skill
    project = ActiveProject("software", "Test ICE", 2, 100, 100)
    character.active_project = project
    character.skills["Programming"] = 8
    mock_character_repo.get.return_value = character
    char_id = CharacterId(character.id)

    # Patch random to guarantee a successful roll
    with patch(
        "decker_pygame.application.project_service.random.randint", return_value=5
    ):
        project_service.complete_project(char_id)

    # Assert: Schematic awarded, project removed
    assert len(character.schematics) == 1
    assert character.schematics[0].name == "Test ICE v2 Schematic"
    assert character.active_project is None
    mock_character_repo.save.assert_called_once_with(character)


def test_complete_project_skill_check_fails(
    project_service: ProjectService, mock_character_repo: Mock, character: Character
):
    """A completed project is consumed but no schematic is awarded on a bad roll."""
    # Setup: Project is finished, character has low skill
    project = ActiveProject("software", "Test ICE", 2, 100, 100)
    character.active_project = project
    character.skills["Programming"] = 1
    mock_character_repo.get.return_value = character
    char_id = CharacterId(character.id)

    # Patch random to guarantee a failed roll
    with patch(
        "decker_pygame.application.project_service.random.randint", return_value=9
    ):
        project_service.complete_project(char_id)

    # Assert: No schematic, project still removed
    assert len(character.schematics) == 0
    assert character.active_project is None
    mock_character_repo.save.assert_called_once_with(character)


def test_complete_project_not_enough_time(
    project_service: ProjectService, mock_character_repo: Mock, character: Character
):
    """Tests that an error is raised if the project isn't finished."""
    # Setup: Project is NOT finished
    project = ActiveProject("software", "Test ICE", 1, 100, 50)
    character.active_project = project
    mock_character_repo.get.return_value = character
    char_id = CharacterId(character.id)

    with pytest.raises(ProjectError, match="not yet complete"):
        project_service.complete_project(char_id)

    mock_character_repo.save.assert_not_called()


def test_get_project_data_with_active_project(
    project_service: ProjectService, mock_character_repo: Mock, character: Character
):
    """Tests that get_project_data returns a DTO for an active project."""
    project = ActiveProject("software", "Test ICE", 2, 100, 50)
    character.active_project = project
    mock_character_repo.get.return_value = character
    char_id = CharacterId(character.id)

    dto = project_service.get_project_data(char_id)

    assert isinstance(dto, ProjectDataViewDTO)
    assert dto.item_class == "Test ICE"
    assert dto.target_rating == 2
    assert dto.time_required == 100
    assert dto.time_spent == 50


def test_get_project_data_with_no_active_project(
    project_service: ProjectService, mock_character_repo: Mock, character: Character
):
    """Tests that get_project_data returns None if no project is active."""
    character.active_project = None
    mock_character_repo.get.return_value = character
    char_id = CharacterId(character.id)

    dto = project_service.get_project_data(char_id)

    assert dto is None


def test_get_project_data_character_not_found(
    project_service: ProjectService, mock_character_repo: Mock
):
    """Tests that get_project_data returns None if character is not found."""
    mock_character_repo.get.return_value = None
    char_id = CharacterId(uuid.uuid4())

    dto = project_service.get_project_data(char_id)

    assert dto is None


def test_get_new_project_data_success(
    project_service: ProjectService, mock_character_repo: Mock, character: Character
):
    """Tests that get_new_project_data returns a DTO with correct skills."""
    character.skills["Programming"] = 5
    character.skills["Chip Design"] = 2
    mock_character_repo.get.return_value = character
    char_id = CharacterId(character.id)

    dto = project_service.get_new_project_data(char_id)

    assert isinstance(dto, NewProjectViewDTO)
    assert dto.programming_skill == 5
    assert dto.chip_design_skill == 2
    assert "Sentry ICE" in dto.available_software
    assert "Cortex Bomb" in dto.available_chips


def test_get_new_project_data_character_not_found(
    project_service: ProjectService, mock_character_repo: Mock
):
    """Tests that get_new_project_data returns None if character is not found."""
    mock_character_repo.get.return_value = None
    char_id = CharacterId(uuid.uuid4())

    dto = project_service.get_new_project_data(char_id)

    assert dto is None


def test_complete_project_no_active_project(
    project_service: ProjectService, mock_character_repo: Mock, character: Character
):
    """Tests that an error is raised if there is no active project."""
    character.active_project = None
    mock_character_repo.get.return_value = character
    char_id = CharacterId(character.id)

    with pytest.raises(ProjectError, match="no active project to complete"):
        project_service.complete_project(char_id)


def test_complete_project_character_not_found(
    project_service: ProjectService, mock_character_repo: Mock
):
    """Tests that an error is raised if the character is not found."""
    mock_character_repo.get.return_value = None
    char_id = CharacterId(uuid.uuid4())

    with pytest.raises(ProjectError, match="not found"):
        project_service.complete_project(char_id)


def test_complete_project_invalid_item_type_in_project(
    project_service: ProjectService, mock_character_repo: Mock, character: Character
):
    """Tests an error is raised if the active project has an invalid type."""
    # Setup: Project is finished but has a corrupted/invalid item_type
    project = ActiveProject("invalid_type", "Test Item", 1, 100, 100)
    character.active_project = project
    mock_character_repo.get.return_value = character
    char_id = CharacterId(character.id)

    with pytest.raises(ProjectError, match="Invalid item type in active project"):
        project_service.complete_project(char_id)

    mock_character_repo.save.assert_not_called()
