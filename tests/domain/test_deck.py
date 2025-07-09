import uuid

import pytest

from decker_pygame.domain.deck import Deck
from decker_pygame.domain.ids import DeckId, ProgramId
from decker_pygame.domain.program import Program


def test_deck_add_program():
    """Tests that adding a program correctly modifies the deck."""
    deck = Deck(id=DeckId(uuid.uuid4()), programs=[])
    assert not deck.programs

    new_program = Program(id=ProgramId(uuid.uuid4()), name="Test Program", size=10)
    deck.add_program(new_program)

    assert len(deck.programs) == 1
    assert deck.programs[0] == new_program


def test_deck_move_program():
    """Tests moving programs up and down in the deck order."""
    p1 = Program(id=ProgramId(uuid.uuid4()), name="Program A", size=10)
    p2 = Program(id=ProgramId(uuid.uuid4()), name="Program B", size=10)
    p3 = Program(id=ProgramId(uuid.uuid4()), name="Program C", size=10)
    deck = Deck(id=DeckId(uuid.uuid4()), programs=[p1, p2, p3])

    # Move B up
    deck.move_program_up("Program B")
    assert deck.programs == [p2, p1, p3]

    # Try to move B up again (it's now first)
    deck.move_program_up("Program B")
    assert deck.programs == [p2, p1, p3]  # No change

    # Move B down
    deck.move_program_down("Program B")
    assert deck.programs == [p1, p2, p3]

    # Move B down again
    deck.move_program_down("Program B")
    assert deck.programs == [p1, p3, p2]

    # Try to move B down again (it's now last)
    deck.move_program_down("Program B")
    assert deck.programs == [p1, p3, p2]  # No change


def test_deck_move_nonexistent_program():
    """Tests that trying to move a non-existent program raises an error."""
    deck = Deck(id=DeckId(uuid.uuid4()), programs=[])
    with pytest.raises(ValueError, match="not found in deck"):
        deck.move_program_up("Non-existent")
    with pytest.raises(ValueError, match="not found in deck"):
        deck.move_program_down("Non-existent")


def test_deck_serialization_roundtrip():
    """Tests that a Deck can be serialized and deserialized correctly."""
    deck_id = DeckId(uuid.uuid4())
    program = Program(id=ProgramId(uuid.uuid4()), name="Test Program", size=10)
    original_deck = Deck(id=deck_id, programs=[program])

    deck_dict = original_deck.to_dict()

    assert deck_dict["id"] == str(deck_id)
    assert len(deck_dict["programs"]) == 1
    assert deck_dict["programs"][0]["name"] == "Test Program"

    reconstituted_deck = Deck.from_dict(deck_dict)

    assert reconstituted_deck == original_deck
    assert reconstituted_deck.id == original_deck.id
    assert reconstituted_deck.programs == original_deck.programs
