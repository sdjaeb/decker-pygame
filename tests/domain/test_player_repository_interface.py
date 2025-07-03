import uuid
from unittest.mock import Mock, patch

import pytest

from decker_pygame.domain.player import Player, PlayerId
from decker_pygame.domain.player_repository_interface import PlayerRepositoryInterface


def test_abstract_repository_methods_raise_error():
    """Covers the abstract methods in the repository ABC."""
    with patch.object(PlayerRepositoryInterface, "__abstractmethods__", set()):
        # Ignore the abstract usage error because the patch makes it instantiable
        # at runtime.
        repo = PlayerRepositoryInterface()  # type: ignore[abstract]
        with pytest.raises(NotImplementedError):
            repo.get(PlayerId(uuid.uuid4()))
        with pytest.raises(NotImplementedError):
            # Pass a mock object that respects the type hint for Player
            mock_player = Mock(spec=Player)
            repo.save(player=mock_player)
