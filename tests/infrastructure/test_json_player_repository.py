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


def test_save_and_get_player():
    """Tests that a player can be saved and retrieved."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = JsonFilePlayerRepository(base_path=tmpdir)
        player_id = PlayerId(uuid.uuid4())
        player = Player(id=player_id, name="Test Player", health=100)

        repo.save(player)

        retrieved_player = repo.get(player_id)

        assert retrieved_player is not None
        assert retrieved_player.id == player.id
        assert retrieved_player.name == "Test Player"


def test_repository_get_returns_none_for_nonexistent_player():
    """Verify that getting a non-existent player returns None."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = JsonFilePlayerRepository(base_path=tmpdir)
        non_existent_id = PlayerId(uuid.uuid4())
        assert repo.get(non_existent_id) is None
