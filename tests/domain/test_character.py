import uuid

from decker_pygame.domain.character import Character
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
        credits=1000,
    )

    char_dict = original_char.to_dict()

    reconstituted_char = Character.from_dict(char_dict)

    assert reconstituted_char == original_char
    assert reconstituted_char.name == original_char.name
    assert reconstituted_char.skills == original_char.skills
    assert reconstituted_char.inventory == original_char.inventory
    assert reconstituted_char.credits == original_char.credits
