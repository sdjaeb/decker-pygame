import uuid
from unittest.mock import Mock, patch

import pytest

from decker_pygame.application.dtos import NewProjectViewDTO
from decker_pygame.application.event_dispatcher import EventDispatcher
from decker_pygame.application.project_service import ProjectError, ProjectService
from decker_pygame.domain.character import Character
from decker_pygame.domain.crafting import RequiredResource, Schematic
from decker_pygame.domain.ids import CharacterId, DeckId, SchematicId
from decker_pygame.domain.project import ActiveProject, ProjectType
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
def project_service(
    mock_character_repo: Mock, mock_event_dispatcher: Mock
) -> ProjectService:
    """Provides a ProjectService instance with a mock repository."""
    return ProjectService(mock_character_repo, mock_event_dispatcher)


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
    assert project.project_type == ProjectType.SOFTWARE
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
    character.schematics.append(
        Schematic(
            id=SchematicId(uuid.uuid4()),
            type=ProjectType.SOFTWARE,
            name="Test ICE v2",
            produces_item_name="Test ICE",
            produces_item_size=40,
            rating=2,
            cost=[],
        )
    )
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
    project = ActiveProject(
        project_type=ProjectType.SOFTWARE,
        item_class="Test ICE",
        target_rating=1,
        time_required=100,
        time_spent=25,
    )
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
    project = ActiveProject(
        project_type=ProjectType.SOFTWARE,
        item_class="Test ICE",
        target_rating=2,
        time_required=100,
        time_spent=100,
    )
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
    project = ActiveProject(
        project_type=ProjectType.SOFTWARE,
        item_class="Test ICE",
        target_rating=2,
        time_required=100,
        time_spent=100,
    )
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
    project = ActiveProject(
        project_type=ProjectType.SOFTWARE,
        item_class="Test ICE",
        target_rating=1,
        time_required=100,
        time_spent=50,
    )
    character.active_project = project
    mock_character_repo.get.return_value = character
    char_id = CharacterId(character.id)

    with pytest.raises(ProjectError, match="not yet complete"):
        project_service.complete_project(char_id)

    mock_character_repo.save.assert_not_called()


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


def test_get_project_data_view_data_with_active_project(
    project_service: ProjectService, mock_character_repo: Mock, character: Character
):
    """
    Tests that the service returns a correct DTO for a character with an active project.
    """
    project = ActiveProject(
        project_type=ProjectType.SOFTWARE,
        item_class="Test ICE",
        target_rating=2,
        time_required=100,
        time_spent=50,
    )
    character.active_project = project
    character.schematics.append(
        Schematic(
            id=SchematicId(uuid.uuid4()),
            type=ProjectType.SOFTWARE,
            name="Known Schematic",
            produces_item_name="Known Item",
            produces_item_size=1,
            rating=1,
            cost=[],
        )
    )
    mock_character_repo.get.return_value = character
    char_id = CharacterId(character.id)

    dto = project_service.get_project_data_view_data(char_id)

    assert dto is not None
    assert dto.project_type == "Test ICE - 2"
    assert dto.project_time_left == "50 TU"
    assert dto.can_work_on_project is True
    assert dto.can_start_new_project is False
    assert len(dto.source_codes) == 1
    assert dto.source_codes[0].name == "Known Item"


def test_get_project_data_view_data_no_project(
    project_service: ProjectService, mock_character_repo: Mock, character: Character
):
    """Tests that the service returns a correct DTO for a character with no project."""
    character.active_project = None
    mock_character_repo.get.return_value = character
    char_id = CharacterId(character.id)

    dto = project_service.get_project_data_view_data(char_id)

    assert dto is not None
    assert dto.project_type == "None"
    assert dto.project_time_left == ""
    assert dto.can_work_on_project is False
    assert dto.can_start_new_project is True


def test_get_project_data_view_data_character_not_found(
    project_service: ProjectService, mock_character_repo: Mock
):
    """Tests that get_project_data_view_data returns None if character is not found."""
    mock_character_repo.get.return_value = None
    char_id = CharacterId(uuid.uuid4())

    dto = project_service.get_project_data_view_data(char_id)

    assert dto is None


def test_build_from_schematic_success(
    project_service: ProjectService,
    mock_character_repo: Mock,
    mock_event_dispatcher: Mock,
    character: Character,
):
    """Tests that an item can be successfully built from a schematic by ID."""
    schematic = Schematic(
        id=SchematicId(uuid.uuid4()),
        type=ProjectType.SOFTWARE,
        name="Test Build",
        produces_item_name="Built Item",
        produces_item_size=1,
        rating=1,
        cost=[RequiredResource("credits", 100)],
    )
    character.schematics.append(schematic)
    character.credits = 200
    mock_character_repo.get.return_value = character
    char_id = CharacterId(character.id)

    project_service.build_from_schematic(char_id, str(schematic.id))

    assert character.credits == 100
    assert len(character.stored_programs) == 1
    assert character.stored_programs[0].name == "Built Item"
    mock_character_repo.save.assert_called_once_with(character)
    mock_event_dispatcher.dispatch.assert_called_once()


def test_build_from_schematic_not_found(
    project_service: ProjectService, mock_character_repo: Mock, character: Character
):
    """Tests building from a non-existent schematic ID raises an error."""
    mock_character_repo.get.return_value = character
    char_id = CharacterId(character.id)
    non_existent_id = str(uuid.uuid4())

    with pytest.raises(ProjectError, match="not found for character"):
        project_service.build_from_schematic(char_id, non_existent_id)


def test_build_from_schematic_character_not_found(
    project_service: ProjectService, mock_character_repo: Mock
):
    """Tests building from schematic fails if the character is not found."""
    mock_character_repo.get.return_value = None
    char_id = CharacterId(uuid.uuid4())

    with pytest.raises(ProjectError, match="Character with ID .* not found."):
        project_service.build_from_schematic(char_id, str(uuid.uuid4()))


def test_build_from_schematic_craft_error(
    project_service: ProjectService, mock_character_repo: Mock, character: Character
):
    """Tests that a ValueError during craft is re-raised as ProjectError."""
    schematic = Schematic(
        id=SchematicId(uuid.uuid4()),
        type=ProjectType.SOFTWARE,
        name="Test Build",
        produces_item_name="Built Item",
        produces_item_size=1,
        rating=1,
        cost=[RequiredResource("credits", 100)],
    )
    character.schematics.append(schematic)
    mock_character_repo.get.return_value = character
    char_id = CharacterId(character.id)

    with patch.object(
        character, "craft", side_effect=ValueError("Not enough resources")
    ):
        with pytest.raises(ProjectError, match="Not enough resources"):
            project_service.build_from_schematic(char_id, str(schematic.id))


def test_trash_schematic_success(
    project_service: ProjectService, mock_character_repo: Mock, character: Character
):
    """Tests that a schematic can be successfully trashed by ID."""
    schematic = Schematic(
        id=SchematicId(uuid.uuid4()),
        type=ProjectType.SOFTWARE,
        name="To Trash",
        produces_item_name="Junk",
        produces_item_size=1,
        rating=1,
        cost=[],
    )
    character.schematics.append(schematic)
    mock_character_repo.get.return_value = character
    char_id = CharacterId(character.id)

    project_service.trash_schematic(char_id, str(schematic.id))

    assert len(character.schematics) == 0
    mock_character_repo.save.assert_called_once_with(character)


def test_trash_schematic_not_found(
    project_service: ProjectService, mock_character_repo: Mock, character: Character
):
    """Tests trashing a non-existent schematic ID raises an error."""
    mock_character_repo.get.return_value = character
    char_id = CharacterId(character.id)
    non_existent_id = str(uuid.uuid4())

    with pytest.raises(ProjectError, match="not found for character"):
        project_service.trash_schematic(char_id, non_existent_id)


def test_trash_schematic_character_not_found(
    project_service: ProjectService, mock_character_repo: Mock
):
    """Tests trashing a schematic fails if the character is not found."""
    mock_character_repo.get.return_value = None
    char_id = CharacterId(uuid.uuid4())

    with pytest.raises(ProjectError, match="Character with ID .* not found."):
        project_service.trash_schematic(char_id, str(uuid.uuid4()))


def test_complete_project_invalid_item_type_in_active_project(
    project_service: ProjectService, mock_character_repo: Mock, character: Character
):
    """Tests that an error is raised if the active project has an invalid item type."""
    project = ActiveProject(
        project_type=Mock(),  # Mock an invalid project type
        item_class="Test ICE",
        target_rating=2,
        time_required=100,
        time_spent=100,
    )
    project.project_type.value = "invalid_type"
    character.active_project = project
    mock_character_repo.get.return_value = character
    char_id = CharacterId(character.id)

    with pytest.raises(ProjectError, match="Invalid item type in active project"):
        project_service.complete_project(char_id)
