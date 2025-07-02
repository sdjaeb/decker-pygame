import uuid
from unittest.mock import patch

import pytest

from decker_pygame.domain.model import PlayerId
from decker_pygame.domain.repositories import PlayerRepository


def test_abstract_repository_methods_raise_error():
    """Covers the abstract methods in the repository ABC."""
    with patch.object(PlayerRepository, "__abstractmethods__", set()):
        repo = PlayerRepository()
        with pytest.raises(NotImplementedError):
            repo.get(PlayerId(uuid.uuid4()))
        with pytest.raises(NotImplementedError):
            repo.save(player=None)
