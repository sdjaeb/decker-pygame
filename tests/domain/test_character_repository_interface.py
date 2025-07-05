import uuid
from unittest.mock import Mock, patch

import pytest

from decker_pygame.domain.character import Character
from decker_pygame.domain.character_repository_interface import (
    CharacterRepositoryInterface,
)
from decker_pygame.domain.ids import CharacterId


def test_abstract_repository_methods_raise_error():
    """Covers the abstract methods in the repository ABC."""
    with patch.object(CharacterRepositoryInterface, "__abstractmethods__", set()):
        repo = CharacterRepositoryInterface()  # type: ignore[abstract]
        with pytest.raises(NotImplementedError):
            repo.get(CharacterId(uuid.uuid4()))
        with pytest.raises(NotImplementedError):
            mock_character = Mock(spec=Character)
            repo.save(character=mock_character)
