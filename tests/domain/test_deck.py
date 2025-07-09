import uuid

import pytest

from decker_pygame.domain.deck import Deck
from decker_pygame.domain.ids import DeckId, ProgramId
from decker_pygame.domain.program import Program


@pytest.fixture
def deck() -> Deck:
    """Returns a deck instance for testing."""
    return Deck(id=DeckId(uuid.uuid4()), programs=[])


def test_add_program(deck: Deck):
    """Tests that a program can be added to the deck."""
    program = Program(id=ProgramId(uuid.uuid4()), name="TestProg", size=10)
    deck.add_program(program)
    assert len(deck.programs) == 1
    assert deck.programs[0] is program


def test_remove_program_success(deck: Deck):
    """Tests that a program can be successfully removed from the deck."""
    program = Program(id=ProgramId(uuid.uuid4()), name="TestProg", size=10)
    deck.programs.append(program)

    assert len(deck.programs) == 1

    removed_program = deck.remove_program("TestProg")

    assert len(deck.programs) == 0
    assert removed_program is program


def test_remove_program_not_found(deck: Deck):
    """Tests that removing a non-existent program raises a ValueError."""
    with pytest.raises(ValueError, match="not found in deck"):
        deck.remove_program("NonExistent")


def test_move_program_up_and_down(deck: Deck):
    """Tests moving programs within the deck."""
    p1 = Program(id=ProgramId(uuid.uuid4()), name="P1", size=1)
    p2 = Program(id=ProgramId(uuid.uuid4()), name="P2", size=1)
    p3 = Program(id=ProgramId(uuid.uuid4()), name="P3", size=1)
    deck.programs = [p1, p2, p3]

    # Move P2 up
    deck.move_program_up("P2")
    assert deck.programs == [p2, p1, p3]

    # Move P2 down
    deck.move_program_down("P2")
    assert deck.programs == [p1, p2, p3]


def test_move_program_at_boundaries(deck: Deck):
    """Tests moving programs at the top or bottom of the list."""
    p1 = Program(id=ProgramId(uuid.uuid4()), name="P1", size=1)
    p2 = Program(id=ProgramId(uuid.uuid4()), name="P2", size=1)
    deck.programs = [p1, p2]

    # Moving top item up should do nothing
    deck.move_program_up("P1")
    assert deck.programs == [p1, p2]

    # Moving bottom item down should do nothing
    deck.move_program_down("P2")
    assert deck.programs == [p1, p2]


def test_move_nonexistent_program(deck: Deck):
    """Tests that moving a non-existent program raises an error."""
    with pytest.raises(ValueError, match="not found in deck"):
        deck.move_program_up("NonExistent")
    with pytest.raises(ValueError, match="not found in deck"):
        deck.move_program_down("NonExistent")
