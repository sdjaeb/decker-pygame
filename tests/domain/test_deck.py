import uuid

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
