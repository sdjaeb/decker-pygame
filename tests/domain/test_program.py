import uuid

from decker_pygame.domain.ids import ProgramId
from decker_pygame.domain.program import Program


def test_program_creation():
    """Tests creating a Program entity."""
    program_id = ProgramId(uuid.uuid4())
    program = Program(id=program_id, name="Hammer")

    assert program.id == program_id
    assert program.name == "Hammer"


def test_program_equality_and_hashing():
    """Tests that program equality and hashing are based on ID."""
    program_id = ProgramId(uuid.uuid4())
    program1 = Program(id=program_id, name="Hammer")
    program2 = Program(id=program_id, name="Different Name")
    program3 = Program(id=ProgramId(uuid.uuid4()), name="Hammer")

    # Test equality
    assert program1 == program2
    assert program1 != program3
    assert program1 != "not a program"

    # Test hashing and set behavior
    program_set = {program1, program2}
    assert len(program_set) == 1
    assert program1 in program_set
    assert program3 not in program_set
