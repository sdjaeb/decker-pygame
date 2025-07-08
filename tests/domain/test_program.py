import uuid

from decker_pygame.domain.ids import ProgramId
from decker_pygame.domain.program import Program


def test_program_serialization_roundtrip():
    """Tests that a Program entity can be serialized and deserialized correctly."""
    program_id = ProgramId(uuid.uuid4())
    original_program = Program(id=program_id, name="Hammer", size=10)

    program_dict = original_program.to_dict()

    assert program_dict == {"id": str(program_id), "name": "Hammer", "size": 10}

    reconstituted_program = Program.from_dict(program_dict)

    assert reconstituted_program == original_program
    assert reconstituted_program.name == original_program.name
    assert reconstituted_program.size == original_program.size
