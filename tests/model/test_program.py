import pytest
from pydantic import ValidationError

from decker_pygame.model.enums import ProgramType
from decker_pygame.model.program import Program


def test_program_creation():
    """Tests basic creation of a Program instance."""
    program = Program(
        name="Deception",
        type=ProgramType.STEALTH,
        size=10,
        cost=500,
        description="A simple stealth program.",
    )
    assert program.name == "Deception"
    assert program.type == ProgramType.STEALTH
    assert program.size == 10
    assert program.cost == 500
    assert program.description == "A simple stealth program."


def test_program_validation():
    """Tests that invalid values raise a validation error."""
    # Test non-positive size
    with pytest.raises(ValidationError):
        Program(
            name="BadSize", type=ProgramType.ATTACK, size=0, cost=100, description="..."
        )

    # Test negative cost
    with pytest.raises(ValidationError):
        Program(
            name="BadCost",
            type=ProgramType.UTILITY,
            size=5,
            cost=-100,
            description="...",
        )
