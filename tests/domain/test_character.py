import uuid

from decker_pygame.domain.character import Character, CharacterId
from decker_pygame.domain.events import CharacterCreated


def test_character_creation_raises_event():
    """Verify that creating a character adds a CharacterCreated event."""
    char_id = CharacterId(uuid.uuid4())
    name = "Test Character"

    char = Character.create(character_id=char_id, name=name)

    assert len(char.events) == 1
    event = char.events[0]
    assert isinstance(event, CharacterCreated)
    assert event.character_id == char_id
    assert event.name == name


def test_character_equality():
    """Characters should be equal if they have the same ID."""
    char_id = CharacterId(uuid.uuid4())
    char1 = Character(char_id, "char1", {}, [], 100)
    char2 = Character(char_id, "char2", {"hacking": 1}, [], 200)
    char3 = Character(CharacterId(uuid.uuid4()), "char1", {}, [], 100)

    assert char1 == char2
    assert char1 != char3
    assert char1 != "not a character"


def test_character_hash():
    """Characters with the same ID should have the same hash."""
    char_id = CharacterId(uuid.uuid4())
    char1 = Character(char_id, "char1", {}, [], 100)
    char2 = Character(char_id, "char2", {"hacking": 1}, [], 200)

    assert hash(char1) == hash(char2)
    assert len({char1, char2}) == 1
