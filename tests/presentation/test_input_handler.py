from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.ports.service_interfaces import LoggingServiceInterface
from decker_pygame.presentation.debug_actions import DebugActions
from decker_pygame.presentation.game import Game
from decker_pygame.presentation.input_handler import PygameInputHandler


@pytest.fixture
def mock_game() -> Mock:
    """Provides a mock Game object with mock views."""
    game = Mock(spec=Game)
    # The input handler now depends on the view_manager.modal_stack attribute.
    game.view_manager = Mock()
    game.view_manager.modal_stack = []
    return game


@pytest.fixture
def mock_logging_service() -> Mock:
    """Provides a mock LoggingService."""
    return Mock(spec=LoggingServiceInterface)


@pytest.fixture
def mock_debug_actions() -> Mock:
    """Provides a mock DebugActions object."""
    return Mock(spec=DebugActions)


def test_handle_quit_event(
    mock_game: Mock, mock_logging_service: Mock, mock_debug_actions: Mock
):
    """Tests that a QUIT event calls game.quit()."""
    handler = PygameInputHandler(mock_game, mock_logging_service, mock_debug_actions)
    quit_event = pygame.event.Event(pygame.QUIT)

    with patch("pygame.event.get", return_value=[quit_event]):
        handler.handle_events()

    mock_game.quit.assert_called_once()


@pytest.mark.parametrize(
    "key, method_name, is_debug_action",
    [
        (pygame.K_h, "toggle_home_view", True),
        (pygame.K_r, "toggle_matrix_run_view", False),
        (pygame.K_m, "log_matrix_event", True),
        (pygame.K_q, "quit", False),
    ],
)
def test_handle_keydown_events(
    key: int,
    method_name: str,
    is_debug_action: bool,
    mock_game: Mock,
    mock_logging_service: Mock,
    mock_debug_actions: Mock,
):
    """Tests that keydown events call the correct methods on the game object."""
    handler = PygameInputHandler(mock_game, mock_logging_service, mock_debug_actions)
    key_event = pygame.event.Event(pygame.KEYDOWN, {"key": key})

    with patch("pygame.event.get", return_value=[key_event]):
        handler.handle_events()

    if is_debug_action:
        target_mock = mock_debug_actions
    else:
        target_mock = mock_game

    method_to_check = getattr(target_mock, method_name)
    method_to_check.assert_called_once()


def test_handle_unmapped_keydown(
    mock_game: Mock, mock_logging_service: Mock, mock_debug_actions: Mock
):
    """Tests that a keydown event not in the map does nothing."""
    handler = PygameInputHandler(mock_game, mock_logging_service, mock_debug_actions)
    # Use a key that is not in the handler's key_map
    unmapped_key_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_x})

    with patch("pygame.event.get", return_value=[unmapped_key_event]):
        handler.handle_events()

    # Assert that no game methods were called
    mock_game.toggle_build_view.assert_not_called()
    mock_game.toggle_char_data_view.assert_not_called()
    mock_game.quit.assert_not_called()


def test_handle_events_delegates_to_top_modal_view(
    mock_game: Mock, mock_logging_service: Mock, mock_debug_actions: Mock
):
    """Tests that events are delegated only to the top-most view on the modal stack."""
    handler = PygameInputHandler(mock_game, mock_logging_service, mock_debug_actions)
    mouse_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN)

    # Create mock views that conform to the Eventful protocol
    view1 = Mock(spec=["handle_event"])
    view2 = Mock(spec=["handle_event"])
    mock_game.view_manager.modal_stack = [view1, view2]

    with patch("pygame.event.get", return_value=[mouse_event]):
        handler.handle_events()

    # Only the top view (view2) should receive the event
    view1.handle_event.assert_not_called()
    view2.handle_event.assert_called_once_with(mouse_event)


def test_logs_keypress_in_dev_mode(
    mock_game: Mock, mock_logging_service: Mock, mock_debug_actions: Mock
):
    """Tests that keypresses are logged when dev mode is enabled."""
    handler = PygameInputHandler(mock_game, mock_logging_service, mock_debug_actions)

    with patch("decker_pygame.presentation.input_handler.DEV_SETTINGS.enabled", True):
        key_event = pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_a})
        with patch("pygame.event.get", return_value=[key_event]):
            handler.handle_events()

    mock_logging_service.log.assert_called_once_with("Key Press", {"key": "a"})
