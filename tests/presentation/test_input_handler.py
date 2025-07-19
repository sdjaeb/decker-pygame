from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.ports.service_interfaces import LoggingServiceInterface
from decker_pygame.presentation.game import Game
from decker_pygame.presentation.input_handler import PygameInputHandler


@pytest.fixture
def mock_game() -> Mock:
    """Provides a mock Game object with mock views."""
    game = Mock(spec=Game)
    game.build_view = Mock()
    game.char_data_view = Mock()
    game.deck_view = Mock()
    game.transfer_view = Mock()
    game.shop_view = Mock()
    game.order_view = Mock()
    game.contract_list_view = Mock()
    game.contract_data_view = Mock()
    game.ice_data_view = Mock()
    game.options_view = Mock()
    game.sound_edit_view = Mock()
    return game


@pytest.fixture
def mock_logging_service() -> Mock:
    """Provides a mock LoggingService."""
    return Mock(spec=LoggingServiceInterface)


def test_handle_quit_event(mock_game: Mock, mock_logging_service: Mock):
    """Tests that a QUIT event calls game.quit()."""
    handler = PygameInputHandler(mock_game, mock_logging_service)
    quit_event = pygame.event.Event(pygame.QUIT)

    with patch("pygame.event.get", return_value=[quit_event]):
        handler.handle_events()

    mock_game.quit.assert_called_once()


@pytest.mark.parametrize(
    "key, method_name",
    [
        (pygame.K_b, "toggle_build_view"),
        (pygame.K_c, "toggle_char_data_view"),
        (pygame.K_l, "toggle_contract_list_view"),
        (pygame.K_d, "toggle_contract_data_view"),
        (pygame.K_p, "toggle_deck_view"),
        (pygame.K_o, "toggle_options_view"),
        (pygame.K_u, "toggle_sound_edit_view"),
        (pygame.K_q, "quit"),
    ],
)
def test_handle_keydown_events(
    key: int, method_name: str, mock_game: Mock, mock_logging_service: Mock
):
    """Tests that keydown events call the correct methods on the game object."""
    handler = PygameInputHandler(mock_game, mock_logging_service)
    key_event = pygame.event.Event(pygame.KEYDOWN, {"key": key})

    with patch("pygame.event.get", return_value=[key_event]):
        handler.handle_events()

    method_to_check = getattr(mock_game, method_name)
    method_to_check.assert_called_once()


def test_handle_unmapped_keydown(mock_game: Mock, mock_logging_service: Mock):
    """Tests that a keydown event not in the map does nothing."""
    handler = PygameInputHandler(mock_game, mock_logging_service)
    # Use a key that is not in the handler's key_map
    unmapped_key_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_x})

    with patch("pygame.event.get", return_value=[unmapped_key_event]):
        handler.handle_events()

    # Assert that no game methods were called
    mock_game.toggle_build_view.assert_not_called()
    mock_game.toggle_char_data_view.assert_not_called()
    mock_game.quit.assert_not_called()


def test_delegates_events_to_views(mock_game: Mock, mock_logging_service: Mock):
    """Tests that events are passed to active views."""
    handler = PygameInputHandler(mock_game, mock_logging_service)
    mouse_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN)

    with patch("pygame.event.get", return_value=[mouse_event]):
        handler.handle_events()

    mock_game.build_view.handle_event.assert_called_once_with(mouse_event)
    mock_game.char_data_view.handle_event.assert_called_once_with(mouse_event)
    mock_game.deck_view.handle_event.assert_called_once_with(mouse_event)
    mock_game.transfer_view.handle_event.assert_called_once_with(mouse_event)
    mock_game.shop_view.handle_event.assert_called_once_with(mouse_event)
    mock_game.order_view.handle_event.assert_called_once_with(mouse_event)
    mock_game.contract_list_view.handle_event.assert_called_once_with(mouse_event)
    mock_game.contract_data_view.handle_event.assert_called_once_with(mouse_event)
    mock_game.ice_data_view.handle_event.assert_called_once_with(mouse_event)
    mock_game.options_view.handle_event.assert_called_once_with(mouse_event)
    mock_game.sound_edit_view.handle_event.assert_called_once_with(mouse_event)


def test_logs_keypress_in_dev_mode(mock_game: Mock, mock_logging_service: Mock):
    """Tests that keypresses are logged when dev mode is enabled."""
    handler = PygameInputHandler(mock_game, mock_logging_service)

    with patch("decker_pygame.presentation.input_handler.DEV_SETTINGS.enabled", True):
        key_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_a})
        with patch("pygame.event.get", return_value=[key_event]):
            handler.handle_events()

    mock_logging_service.log.assert_called_once_with("Key Press", {"key": "a"})
