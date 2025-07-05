import uuid

import pytest

from decker_pygame.domain.character import Character
from decker_pygame.domain.crafting import RequiredResource, Schematic
from decker_pygame.domain.events import ItemCrafted
from decker_pygame.domain.ids import CharacterId, ProgramId
from decker_pygame.domain.program import Program


def test_character_creation():
    """Tests the Character.create factory method."""
    char_id = CharacterId(uuid.uuid4())
    char = Character.create(
        character_id=char_id,
        name="Rynn",
        initial_skills={"hacking": 5},
        initial_credits=1000,
    )
    assert char.id == char_id
    assert char.name == "Rynn"
    assert len(char.events) == 1


def test_character_serialization_roundtrip():
    """Tests that a Character can be serialized and deserialized correctly."""
    char_id = CharacterId(uuid.uuid4())
    prog_id = ProgramId(uuid.uuid4())
    program = Program(id=prog_id, name="IcePick")
    original_char = Character(
        id=char_id,
        name="Rynn",
        skills={"hacking": 5, "blades": 3},
        inventory=[program],
        schematics=[],
        credits=1000,
    )

    char_dict = original_char.to_dict()

    reconstituted_char = Character.from_dict(char_dict)

    assert reconstituted_char == original_char
    assert reconstituted_char.name == original_char.name
    assert reconstituted_char.skills == original_char.skills
    assert reconstituted_char.inventory == original_char.inventory
    assert reconstituted_char.credits == original_char.credits


@pytest.fixture
def character_for_crafting() -> Character:
    """Provides a character instance with initial state for crafting tests."""
    return Character(
        id=CharacterId(uuid.uuid4()),
        name="Rynn",
        skills={"crafting": 5},
        inventory=[],
        schematics=[],
        credits=1000,
    )


def test_character_craft_success(character_for_crafting: Character):
    """Tests that a character can successfully craft an item."""
    char = character_for_crafting
    schematic = Schematic(
        name="IcePick Schematic",
        produces_item_name="IcePick",
        cost=[RequiredResource(name="credits", quantity=500)],
    )

    char.craft(schematic)

    assert char.credits == 500
    assert len(char.inventory) == 1
    assert char.inventory[0].name == "IcePick"

    assert len(char.events) == 1
    event = char.events[0]
    assert isinstance(event, ItemCrafted)
    assert event.character_id == char.id
    assert event.schematic_name == "IcePick Schematic"
    assert event.item_name == "IcePick"


def test_character_craft_insufficient_credits(character_for_crafting: Character):
    """Tests that crafting fails if the character has insufficient credits."""
    char = character_for_crafting
    schematic = Schematic(
        name="Expensive Schematic",
        produces_item_name="Gold-Plated Widget",
        cost=[RequiredResource(name="credits", quantity=2000)],
    )

    with pytest.raises(ValueError, match="Insufficient credits"):
        char.craft(schematic)

    # Verify state has not changed
    assert char.credits == 1000
    assert not char.inventory
    assert not char.events
