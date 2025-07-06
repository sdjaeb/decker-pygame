import uuid

import pytest

from decker_pygame.domain.character import Character
from decker_pygame.domain.crafting import RequiredResource, Schematic
from decker_pygame.domain.events import ItemCrafted, SkillDecreased, SkillIncreased
from decker_pygame.domain.ids import CharacterId


@pytest.fixture
def character() -> Character:
    """Returns a character instance for testing."""
    return Character.create(
        character_id=CharacterId(uuid.uuid4()),
        name="Testy",
        initial_skills={"hacking": 2},
        initial_credits=100,
        initial_skill_points=5,
    )


def test_increase_skill_success(character: Character):
    """Tests that a skill can be increased successfully."""
    character.increase_skill("hacking")

    assert character.skills["hacking"] == 3
    assert character.unused_skill_points == 2  # 5 - (2+1) = 2
    skill_event = next(e for e in character.events if isinstance(e, SkillIncreased))
    assert skill_event.skill_name == "hacking"
    assert skill_event.new_level == 3


def test_increase_skill_insufficient_points(character: Character):
    """Tests that increasing a skill fails with insufficient points."""
    character.unused_skill_points = 1
    with pytest.raises(ValueError, match="Not enough skill points."):
        character.increase_skill("hacking")


def test_decrease_skill_success(character: Character):
    """Tests that a skill can be decreased successfully."""
    character.decrease_skill("hacking")

    assert character.skills["hacking"] == 1
    assert character.unused_skill_points == 7  # 5 + 2 = 7
    skill_event = next(e for e in character.events if isinstance(e, SkillDecreased))
    assert skill_event.skill_name == "hacking"
    assert skill_event.new_level == 1


def test_decrease_skill_at_zero(character: Character):
    """Tests that a skill cannot be decreased below zero."""
    character.skills["hacking"] = 0
    with pytest.raises(ValueError, match="Cannot decrease skill below 0."):
        character.decrease_skill("hacking")


def test_modify_nonexistent_skill(character: Character):
    """Tests that modifying a non-existent skill raises an error."""
    with pytest.raises(ValueError, match="Skill 'crafting' does not exist."):
        character.increase_skill("crafting")

    with pytest.raises(ValueError, match="Skill 'crafting' does not exist."):
        character.decrease_skill("crafting")


def test_craft_success(character: Character):
    """Tests that an item can be crafted successfully."""
    schematic = Schematic(
        name="IcePick v1",
        produces_item_name="IcePick v1",
        cost=[RequiredResource(name="credits", quantity=50)],
    )

    initial_credits = character.credits
    initial_inventory_size = len(character.inventory)

    character.craft(schematic)

    assert character.credits == initial_credits - 50
    assert len(character.inventory) == initial_inventory_size + 1
    assert character.inventory[-1].name == "IcePick v1"

    craft_event = next(e for e in character.events if isinstance(e, ItemCrafted))
    assert craft_event.schematic_name == "IcePick v1"
    assert craft_event.item_name == "IcePick v1"


def test_craft_insufficient_credits(character: Character):
    """Tests that crafting fails if the character has insufficient credits."""
    schematic = Schematic(
        name="Expensive Thing",
        produces_item_name="Expensive Thing",
        cost=[RequiredResource(name="credits", quantity=9999)],
    )
    character.credits = 100

    with pytest.raises(ValueError, match="Insufficient credits"):
        character.craft(schematic)
