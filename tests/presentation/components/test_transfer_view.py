from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.application.deck_service import DeckProgramDTO, TransferViewData
from decker_pygame.presentation.components.button import Button
from decker_pygame.presentation.components.transfer_view import TransferView


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


def test_transfer_view_initialization():
    """Tests that the TransferView initializes and renders its data."""
    mock_on_close = Mock()
    view_data = TransferViewData(
        stored_programs=[DeckProgramDTO(name="IcePick", size=10)],
        deck_programs=[DeckProgramDTO(name="Hammer", size=20)],
    )

    with (
        patch("pygame.font.Font") as mock_font_class,
        patch(
            "decker_pygame.presentation.components.transfer_view.Button"
        ) as mock_button_class,
    ):
        mock_font_instance = Mock()
        mock_font_instance.render.return_value = pygame.Surface((100, 20))
        mock_font_instance.get_linesize.return_value = 20
        mock_font_class.return_value = mock_font_instance

        mock_button_instance = Mock(spec=Button)
        mock_button_instance.image = pygame.Surface((10, 10))
        mock_button_instance.rect = pygame.Rect(0, 0, 10, 10)
        mock_button_class.return_value = mock_button_instance

        view = TransferView(data=view_data, on_close=mock_on_close)

        assert view is not None
        # 2 programs rendered
        assert mock_font_instance.render.call_count == 2
        render_calls = mock_font_instance.render.call_args_list
        rendered_texts = [call.args[0] for call in render_calls]
        assert "- IcePick (10MB)" in rendered_texts
        assert "- Hammer (20MB)" in rendered_texts

        mock_button_class.assert_called_once()
