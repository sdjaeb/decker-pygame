import json
import uuid
from pathlib import Path

from decker_pygame.domain.character import Character
from decker_pygame.domain.ids import CharacterId
from decker_pygame.infrastructure.json_character_repository import (
    JsonFileCharacterRepository,
)


def test_save_and_get_character(tmp_path: Path):
    """
    Tests that a character can be saved and then retrieved correctly.
    """
    # Arrange
    repo = JsonFileCharacterRepository(base_path=str(tmp_path))
    char_id = CharacterId(uuid.uuid4())
    original_char = Character(
        id=char_id,
        name="Rynn",
        skills={"hacking": 5},
        inventory=[],
        schematics=[],
        credits=1000,
    )

    # Act
    repo.save(original_char)
    retrieved_char = repo.get(char_id)

    # Assert
    assert retrieved_char is not None
    assert retrieved_char.id == original_char.id
    assert retrieved_char.name == original_char.name
    assert retrieved_char.credits == original_char.credits

    # Verify the file content
    expected_path = tmp_path / f"{char_id}.json"
    assert expected_path.exists()
    with open(expected_path) as f:
        data = json.load(f)
        assert data["name"] == "Rynn"


def test_get_non_existent_character(tmp_path: Path):
    """Tests that getting a non-existent character returns None."""
    repo = JsonFileCharacterRepository(base_path=str(tmp_path))
    non_existent_id = CharacterId(uuid.uuid4())

    assert repo.get(non_existent_id) is None
