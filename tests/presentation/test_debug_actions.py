"""Tests for the DebugActions class."""

from unittest.mock import Mock

import pytest

from decker_pygame.application.event_dispatcher import EventDispatcher
from decker_pygame.domain.events import MatrixLogEntryCreated
from decker_pygame.presentation.debug_actions import DebugActions
from decker_pygame.presentation.game import Game


@pytest.fixture
def mock_game() -> Mock:
    """Provides a mock Game object."""
    return Mock(spec=Game)


@pytest.fixture
def mock_event_dispatcher() -> Mock:
    """Provides a mock EventDispatcher."""
    return Mock(spec=EventDispatcher)


def test_log_matrix_event(mock_game: Mock, mock_event_dispatcher: Mock):
    """Tests that log_matrix_event dispatches the correct event."""
    actions = DebugActions(game=mock_game, event_dispatcher=mock_event_dispatcher)

    actions.log_matrix_event()

    mock_event_dispatcher.dispatch.assert_called_once()
    dispatched_events = mock_event_dispatcher.dispatch.call_args[0][0]
    assert len(dispatched_events) == 1
    event = dispatched_events[0]
    assert isinstance(event, MatrixLogEntryCreated)
    assert event.message == "[DEBUG] ICE Detected: Sentry v2.0"
    mock_game.show_message.assert_called_once_with("Dispatched debug matrix event.")


def test_toggle_home_view(mock_game: Mock, mock_event_dispatcher: Mock):
    """Tests that toggle_home_view calls the game's method."""
    actions = DebugActions(game=mock_game, event_dispatcher=mock_event_dispatcher)
    actions.toggle_home_view()
    mock_game.toggle_home_view.assert_called_once()
