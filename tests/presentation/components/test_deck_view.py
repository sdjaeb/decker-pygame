from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.application.deck_service import DeckProgramDTO, DeckViewData
from decker_pygame.presentation.components.button import Button
from decker_pygame.presentation.components.deck_view import DeckView


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


def test_deck_view_initialization():
    """Tests that the DeckView initializes and renders its data."""
    mock_on_close = Mock()
    mock_on_order = Mock()
    view_data = DeckViewData(
        programs=[
            DeckProgramDTO(name="IcePick", size=10),
            DeckProgramDTO(name="Hammer", size=20),
        ],
        used_deck_size=30,
        total_deck_size=100,
    )

    with (
        patch("pygame.font.Font") as mock_font_class,
        patch(
            "decker_pygame.presentation.components.deck_view.Button"
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

        view = DeckView(data=view_data, on_close=mock_on_close, on_order=mock_on_order)

        assert view is not None
        # Title + 2 programs
        assert mock_font_instance.render.call_count == 3
        render_calls = mock_font_instance.render.call_args_list
        rendered_texts = [call.args[0] for call in render_calls]
        assert "Deck Memory: 30 / 100" in rendered_texts
        assert "- IcePick (10MB)" in rendered_texts
        assert "- Hammer (20MB)" in rendered_texts

        # Close button + Order button
        assert mock_button_class.call_count == 2


def test_deck_view_close_button_click():
    """Tests that the view correctly delegates events to its close button."""
    mock_on_close = Mock()
    mock_on_order = Mock()
    view_data = DeckViewData(programs=[])

    # Patch dependencies to isolate the test
    with (
        patch("pygame.font.Font") as mock_font_class,
        patch(
            "decker_pygame.presentation.components.deck_view.Button"
        ) as mock_button_class,
    ):
        # Configure the mock font to return a valid surface
        mock_font_instance = Mock()
        mock_font_instance.render.return_value = pygame.Surface((100, 20))
        mock_font_instance.get_linesize.return_value = 20
        mock_font_class.return_value = mock_font_instance

        # Configure the mock button to have the necessary attributes for rendering.
        mock_button_instance = Mock(spec=Button)
        mock_button_instance.image = pygame.Surface((10, 10))
        mock_button_instance.rect = pygame.Rect(0, 0, 10, 10)
        mock_button_class.return_value = mock_button_instance

        view = DeckView(data=view_data, on_close=mock_on_close, on_order=mock_on_order)

        # We can test the event delegation by checking if the button's method is called
        with patch.object(view._close_button, "handle_event") as mock_button_handler:
            event = pygame.event.Event(
                pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (0, 0)}
            )
            view.handle_event(event)
            mock_button_handler.assert_called_once()
