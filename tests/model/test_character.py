from decker_pygame.model.character import Character
from decker_pygame.model.enums import ProgramType
from decker_pygame.model.program import Program


def test_character_creation_defaults():
    """Tests creating a character with default empty values."""
    char = Character(name="Newbie")
    assert char.name == "Newbie"
    assert char.skills == {}
    assert char.inventory == []
    assert char.credits == 0


def test_character_creation_with_values():
    """Tests creating a character with specific values."""
    program1 = Program(
        name="Hammer", type=ProgramType.ATTACK, size=10, cost=500, description="..."
    )
    skills = {"hacking": 5, "electronics": 3}
    char = Character(name="Jax", skills=skills, inventory=[program1], credits=5000)
    assert char.name == "Jax"
    assert char.skills["hacking"] == 5
    assert len(char.inventory) == 1
    assert char.credits == 5000
