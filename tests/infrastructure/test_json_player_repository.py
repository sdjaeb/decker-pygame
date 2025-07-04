import json
import os
import tempfile
import uuid

from decker_pygame.domain.player import Player, PlayerId
from decker_pygame.infrastructure.json_player_repository import JsonFilePlayerRepository


def test_repository_creates_directory_on_init():
    """Verify the repository creates its base directory if it doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_path = os.path.join(tmpdir, "non_existent_dir")
        assert not os.path.exists(repo_path)

        JsonFilePlayerRepository(base_path=repo_path)

        assert os.path.exists(repo_path)


def test_repository_can_save_and_get_player():
    """Verify that a player can be saved and then retrieved."""
    player_id = PlayerId(uuid.uuid4())
    player = Player(id=player_id, name="Deckard", health=100)

    with tempfile.TemporaryDirectory() as tmpdir:
        repo = JsonFilePlayerRepository(base_path=tmpdir)
        repo.save(player)

        # Assert file system state
        expected_file = os.path.join(tmpdir, f"{player_id}.json")
        assert os.path.exists(expected_file)
        with open(expected_file) as f:
            data = json.load(f)
            assert data["id"] == str(player_id)

        # Assert repository get method
        retrieved_player = repo.get(player_id)
        assert (
            retrieved_player is not None
        )  # Ensure it's not None before checking attributes
        assert retrieved_player == player  # Check equality based on ID
        assert retrieved_player.name == player.name
        assert retrieved_player.health == player.health


def test_repository_get_returns_none_for_nonexistent_player():
    """Verify that getting a non-existent player returns None."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = JsonFilePlayerRepository(base_path=tmpdir)
        non_existent_id = PlayerId(uuid.uuid4())
        assert repo.get(non_existent_id) is None
