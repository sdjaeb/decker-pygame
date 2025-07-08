import os
import shutil
import tempfile
import uuid

from decker_pygame.domain.deck import Deck
from decker_pygame.domain.ids import DeckId
from decker_pygame.infrastructure.json_deck_repository import JsonFileDeckRepository


def test_save_and_get_deck():
    """Tests saving and retrieving a Deck aggregate."""
    base_path = tempfile.mkdtemp()
    try:
        repo = JsonFileDeckRepository(base_path)
        deck_id = DeckId(uuid.uuid4())

        # Test getting a non-existent deck
        assert repo.get(deck_id) is None

        # Create and save a deck
        deck = Deck(id=deck_id, programs=[])
        repo.save(deck)

        # Retrieve and verify the deck
        retrieved_deck = repo.get(deck_id)
        assert retrieved_deck is not None
        assert retrieved_deck.id == deck.id
        assert retrieved_deck.programs == []

        # Test that the file was created
        assert os.path.exists(os.path.join(base_path, f"{deck_id}.json"))

    finally:
        if os.path.exists(base_path):
            shutil.rmtree(base_path)
