import tempfile
import uuid

from decker_pygame.domain.character import Character
from decker_pygame.domain.ids import CharacterId, DeckId
from decker_pygame.infrastructure.json_character_repository import (
    JsonFileCharacterRepository,
)


def test_save_and_get_character():
    """Tests that a character can be saved and retrieved."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = JsonFileCharacterRepository(base_path=tmpdir)
        char_id = CharacterId(uuid.uuid4())
        deck_id = DeckId(uuid.uuid4())
        character = Character(
            id=char_id,
            name="Testy",
            skills={"hacking": 1},
            deck_id=deck_id,
            stored_programs=[],
            schematics=[],
            credits=100,
            unused_skill_points=5,
        )

        repo.save(character)

        retrieved_char = repo.get(char_id)

        assert retrieved_char is not None
        assert retrieved_char.id == character.id
        assert retrieved_char.name == "Testy"
        assert retrieved_char.unused_skill_points == 5


def test_get_nonexistent_character():
    """Tests that get returns None for a non-existent character."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = JsonFileCharacterRepository(base_path=tmpdir)
        char_id = CharacterId(uuid.uuid4())

        retrieved_char = repo.get(char_id)

        assert retrieved_char is None
