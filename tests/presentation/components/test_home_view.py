from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.presentation.components.button import Button
from decker_pygame.presentation.components.home_view import HomeView


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


def test_home_view_initialization():
    """Tests that the HomeView initializes and creates its buttons."""
    mock_on_char = Mock()
    mock_on_deck = Mock()
    mock_on_contracts = Mock()
    mock_on_build = Mock()
    mock_on_shop = Mock()
    mock_on_transfer = Mock()

    with (
        patch("pygame.font.Font") as mock_font_class,
        patch(
            "decker_pygame.presentation.components.home_view.Button"
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

        view = HomeView(
            on_char=mock_on_char,
            on_deck=mock_on_deck,
            on_contracts=mock_on_contracts,
            on_build=mock_on_build,
            on_shop=mock_on_shop,
            on_transfer=mock_on_transfer,
        )

        assert view is not None
        assert mock_font_instance.render.call_count == 1
        assert mock_font_instance.render.call_args[0][0] == "Main Menu"

        # 5 buttons should be created
        assert mock_button_class.call_count == 6
        button_calls = mock_button_class.call_args_list
        button_texts = [call.args[2] for call in button_calls]
        button_callbacks = [call.args[3] for call in button_calls]

        assert "Character" in button_texts
        assert "Deck" in button_texts
        assert "Contracts" in button_texts
        assert "Build" in button_texts
        assert "Shop" in button_texts
        assert "Transfer" in button_texts

        assert mock_on_char in button_callbacks
        assert mock_on_deck in button_callbacks
        assert mock_on_contracts in button_callbacks
        assert mock_on_build in button_callbacks
        assert mock_on_shop in button_callbacks
        assert mock_on_transfer in button_callbacks


def test_home_view_event_handling():
    """Tests that the view correctly delegates events to its components."""
    mock_on_char = Mock()
    mock_on_deck = Mock()
    mock_on_contracts = Mock()
    mock_on_build = Mock()
    mock_on_shop = Mock()
    mock_on_transfer = Mock()

    with (
        patch("pygame.font.Font") as mock_font_class,
        patch(
            "decker_pygame.presentation.components.home_view.Button"
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

        view = HomeView(
            on_char=mock_on_char,
            on_deck=mock_on_deck,
            on_contracts=mock_on_contracts,
            on_build=mock_on_build,
            on_shop=mock_on_shop,
            on_transfer=mock_on_transfer,
        )

        # We can test the event delegation by checking if the button's method is called
        with patch.object(
            view._components.sprites()[0], "handle_event"
        ) as mock_button_handler:
            event = pygame.event.Event(
                pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (0, 0)}
            )
            view.handle_event(event)
            mock_button_handler.assert_called_once()
