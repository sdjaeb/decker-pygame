from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.presentation.components.contract_list_view import (
    ContractListView,
)


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


def test_contract_list_view_initialization():
    """Tests that the ContractListView initializes and renders its data."""
    with patch("pygame.font.Font") as mock_font_class:
        mock_font_instance = Mock()
        mock_font_instance.render.return_value = pygame.Surface((100, 20))
        mock_font_class.return_value = mock_font_instance

        view = ContractListView(
            position=(10, 20),
            size=(300, 200),
        )

        assert view.rect.topleft == (10, 20)
        mock_font_instance.render.assert_called_once_with(
            "Contract List (Placeholder)", True, view._font_color
        )
