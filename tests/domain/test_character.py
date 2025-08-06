"""This module contains tests for the Character domain aggregate."""

import uuid

import pytest

from decker_pygame.domain.character import Character
from decker_pygame.domain.crafting import RequiredResource, Schematic
from decker_pygame.domain.events import ItemCrafted, SkillDecreased, SkillIncreased
from decker_pygame.domain.ids import CharacterId, DeckId, ProgramId, SchematicId
from decker_pygame.domain.program import Program
from decker_pygame.domain.project import ActiveProject, ProjectType


@pytest.fixture
def character() -> Character:
    """Provides a default character instance for testing."""
    return Character.create(
        character_id=CharacterId(uuid.uuid4()),
        name="Test Decker",
        deck_id=DeckId(uuid.uuid4()),
        initial_skills={"hacking": 1},
        initial_credits=1000,
        initial_skill_points=5,
        initial_reputation=0,
    )


@pytest.fixture
def active_project() -> ActiveProject:
    """Provides a default ActiveProject instance for testing."""
    return ActiveProject(
        project_type=ProjectType.SOFTWARE,
        item_class="Sentry ICE",
        target_rating=1,
        time_required=100,
        time_spent=0,
    )


@pytest.fixture
def schematic() -> Schematic:
    """Provides a default Schematic instance for testing."""
    return Schematic(
        id=SchematicId(uuid.uuid4()),
        type=ProjectType.SOFTWARE,
        name="IcePick v1 Schematic",
        produces_item_name="IcePick v1",
        produces_item_size=50,
        rating=1,
        cost=[RequiredResource(name="credits", quantity=200)],
    )


def test_start_new_project(character: Character, active_project: ActiveProject):
    """Tests that a new project can be started."""
    assert character.active_project is None
    character.start_new_project(active_project)

    # Assign to a new variable for robust type narrowing
    project = character.active_project
    assert project is not None
    assert project is active_project
    assert project.time_spent == 0


def test_work_on_project(character: Character, active_project: ActiveProject):
    """Tests that time can be added to an active project."""
    character.start_new_project(active_project)

    project = character.active_project
    assert project is not None

    character.work_on_project(25)
    assert project.time_spent == 25
    character.work_on_project(50)
    assert project.time_spent == 75


def test_work_on_project_raises_error_if_no_project(character: Character):
    """Tests that working on a project raises an error if none is active."""
    assert character.active_project is None
    with pytest.raises(ValueError, match="No active project to work on."):
        character.work_on_project(10)


def test_complete_project(character: Character, active_project: ActiveProject):
    """Tests that a project can be completed."""
    character.start_new_project(active_project)
    assert character.active_project is not None
    character.complete_project()
    assert character.active_project is None


def test_complete_project_raises_error_if_no_project(character: Character):
    """Tests that completing a project raises an error if none is active."""
    assert character.active_project is None
    with pytest.raises(ValueError, match="No active project to complete."):
        character.complete_project()


def test_craft_item_success(character: Character, schematic: Schematic):
    """Tests that an item can be crafted successfully."""
    character.credits = 500
    character.craft(schematic)

    assert character.credits == 300
    assert len(character.stored_programs) == 1
    assert character.stored_programs[0].name == "IcePick v1"
    assert len(character.events) == 2  # CharacterCreated + ItemCrafted
    crafted_event = character.events[-1]
    assert isinstance(crafted_event, ItemCrafted)
    assert crafted_event.schematic_name == "IcePick v1 Schematic"


def test_craft_item_insufficient_credits(character: Character, schematic: Schematic):
    """Tests that crafting fails with insufficient credits."""
    character.credits = 100
    with pytest.raises(ValueError, match="Insufficient credits"):
        character.craft(schematic)
    assert character.credits == 100
    assert len(character.stored_programs) == 0


def test_remove_stored_program(character: Character):
    """Tests that a program can be removed from storage."""
    program = Program(id=ProgramId(uuid.uuid4()), name="TestProgram", size=10)
    character.stored_programs.append(program)

    assert len(character.stored_programs) == 1
    removed_program = character.remove_stored_program("TestProgram")
    assert removed_program is program
    assert len(character.stored_programs) == 0


def test_remove_stored_program_not_found(character: Character):
    """Tests that removing a non-existent program raises an error."""
    with pytest.raises(ValueError, match="not found in storage"):
        character.remove_stored_program("NonExistent")


def test_increase_skill_success(character: Character):
    """Tests that a skill can be increased."""
    character.unused_skill_points = 3
    character.skills["hacking"] = 2

    character.increase_skill("hacking")

    assert character.skills["hacking"] == 3
    assert character.unused_skill_points == 0  # cost was 2+1=3
    assert len(character.events) == 2  # CharacterCreated + SkillIncreased
    skill_event = character.events[-1]
    assert isinstance(skill_event, SkillIncreased)
    assert skill_event.skill_name == "hacking"
    assert skill_event.new_level == 3


def test_increase_skill_not_enough_points(character: Character):
    """Tests that increasing a skill fails with not enough points."""
    character.unused_skill_points = 1
    character.skills["hacking"] = 1

    with pytest.raises(ValueError, match="Not enough skill points"):
        character.increase_skill("hacking")

    assert character.skills["hacking"] == 1
    assert character.unused_skill_points == 1


def test_increase_skill_nonexistent(character: Character):
    """Tests that increasing a non-existent skill fails."""
    with pytest.raises(ValueError, match="does not exist"):
        character.increase_skill("nonexistent")


def test_decrease_skill_success(character: Character):
    """Tests that a skill can be decreased."""
    character.unused_skill_points = 0
    character.skills["hacking"] = 3

    character.decrease_skill("hacking")

    assert character.skills["hacking"] == 2
    assert character.unused_skill_points == 3  # refund was 3
    assert len(character.events) == 2  # CharacterCreated + SkillDecreased
    skill_event = character.events[-1]
    assert isinstance(skill_event, SkillDecreased)
    assert skill_event.skill_name == "hacking"
    assert skill_event.new_level == 2


def test_decrease_skill_at_zero(character: Character):
    """Tests that decreasing a skill at 0 fails."""
    character.skills["hacking"] = 0
    with pytest.raises(ValueError, match="Cannot decrease skill below 0"):
        character.decrease_skill("hacking")
    assert character.skills["hacking"] == 0


def test_decrease_skill_nonexistent(character: Character):
    """Tests that decreasing a non-existent skill fails."""
    with pytest.raises(ValueError, match="does not exist"):
        character.decrease_skill("nonexistent")
