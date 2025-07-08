import os
import shutil
import tempfile
import uuid

from decker_pygame.domain.ids import PlayerId
from decker_pygame.domain.player import Player
from decker_pygame.infrastructure.json_player_repository import (
    JsonFilePlayerRepository,
)


def test_get_by_name_no_directory():
    """Tests that get_by_name returns None if the base directory doesn't exist."""
    # Create a temporary directory, instantiate the repo, then remove the directory
    # to simulate the condition where the path doesn't exist during the call.
    temp_dir = tempfile.mkdtemp()
    repo = JsonFilePlayerRepository(temp_dir)
    shutil.rmtree(temp_dir)
    assert repo.get_by_name("Deckard") is None


def test_get_by_name():
    """Tests retrieving a player by name from a directory with multiple files."""
    base_path = tempfile.mkdtemp()
    try:
        repo = JsonFilePlayerRepository(base_path)

        # Test with an empty directory
        assert repo.get_by_name("Deckard") is None

        # Create some players
        player1_id = PlayerId(uuid.uuid4())
        player1 = Player.create(player1_id, "Deckard", initial_health=100)
        repo.save(player1)

        player2_id = PlayerId(uuid.uuid4())
        player2 = Player.create(player2_id, "Rynn", initial_health=90)
        repo.save(player2)

        # Add a non-json file to ensure it's ignored
        with open(os.path.join(base_path, "ignore.txt"), "w") as f:
            f.write("ignore me")

        # Test finding an existing player
        found_player = repo.get_by_name("Rynn")
        assert found_player is not None
        assert found_player.id == player2.id
        assert found_player.name == "Rynn"
        assert found_player.health == 90

        # Test not finding a non-existent player
        assert repo.get_by_name("Gaff") is None

    finally:
        if os.path.exists(base_path):
            shutil.rmtree(base_path)


def test_get():
    """Tests retrieving a player by ID."""
    base_path = tempfile.mkdtemp()
    try:
        repo = JsonFilePlayerRepository(base_path)
        player_id = PlayerId(uuid.uuid4())

        # Test getting a non-existent player
        assert repo.get(player_id) is None

        # Save a player and then get it
        player = Player.create(player_id, "Deckard", initial_health=100)
        repo.save(player)

        found_player = repo.get(player_id)
        assert found_player is not None
        assert found_player.id == player.id
        assert found_player.name == "Deckard"

    finally:
        if os.path.exists(base_path):
            shutil.rmtree(base_path)
