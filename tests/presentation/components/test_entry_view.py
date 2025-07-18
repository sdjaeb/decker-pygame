"""Tests for the EntryView component."""

from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.application.dtos import EntryViewDTO
from decker_pygame.presentation.components.button import Button
from decker_pygame.presentation.components.entry_view import EntryView
from decker_pygame.presentation.components.text_input import TextInput


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def mock_callbacks() -> dict[str, Mock]:
    """Provides a dictionary of mock callback functions."""
    return {
        "on_submit": Mock(),
        "on_close": Mock(),
    }


@pytest.fixture
def entry_view_data() -> EntryViewDTO:
    """Provides sample data for the EntryView."""
    return EntryViewDTO(prompt="Enter Password:", is_password=True)


@pytest.fixture
def entry_view(
    entry_view_data: EntryViewDTO, mock_callbacks: dict[str, Mock]
) -> EntryView:
    """Provides an EntryView instance for testing."""
    view = EntryView(
        data=entry_view_data,
        on_submit=mock_callbacks["on_submit"],
        on_close=mock_callbacks["on_close"],
    )
    # Manually set text for testing callbacks
    view._text_input.text = "secret"
    return view


def test_entry_view_initialization(entry_view: EntryView):
    """Tests that the view is initialized correctly."""
    assert entry_view.rect.topleft == (200, 200)
    # 1 label, 1 text input, 2 buttons
    assert len(entry_view._components) == 4
    assert isinstance(entry_view._text_input, TextInput)
    assert entry_view._text_input._is_password is True


def test_submit_button_callback(entry_view: EntryView, mock_callbacks: dict[str, Mock]):
    """Tests that clicking the OK button triggers the on_submit callback."""
    ok_button = next(
        c for c in entry_view._components if isinstance(c, Button) and c.text == "OK"
    )

    ok_button._on_click()
    mock_callbacks["on_submit"].assert_called_once_with("secret")


def test_cancel_button_callback(entry_view: EntryView, mock_callbacks: dict[str, Mock]):
    """Tests that clicking the Cancel button triggers the on_close callback."""
    cancel_button = next(
        c
        for c in entry_view._components
        if isinstance(c, Button) and c.text == "Cancel"
    )

    cancel_button._on_click()
    mock_callbacks["on_close"].assert_called_once()


def test_entry_view_handle_event_keyboard(entry_view: EntryView):
    """Tests that keyboard events are passed to child components."""
    mock_text_input = entry_view._text_input
    with patch.object(mock_text_input, "handle_event") as mock_handler:
        key_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a, unicode="a")
        entry_view.handle_event(key_event)
        # The original, untranslated event should be passed for keyboard events
        mock_handler.assert_called_once_with(key_event)


def test_entry_view_update(entry_view: EntryView):
    """Tests that the update method calls update on its children."""
    # Add a mock component to spy on
    mock_component = Mock(spec=pygame.sprite.Sprite)
    # The mock needs 'image' and 'rect' attributes for the draw() call to work.
    mock_component.image = pygame.Surface((1, 1))
    mock_component.rect = pygame.Rect(0, 0, 1, 1)
    entry_view._components.add(mock_component)

    # Call the update method
    entry_view.update()

    # Assert that the mock component's update method was called
    mock_component.update.assert_called_once()


def test_entry_view_handle_event_other_event(entry_view: EntryView):
    """Tests that a generic, non-mouse/key event is passed through."""
    # We can spy on the handle_event method of a real child component.
    mock_text_input = entry_view._text_input
    with patch.object(mock_text_input, "handle_event") as mock_handler:
        # Create a generic event that is not a mouse or key event
        other_event = pygame.event.Event(pygame.USEREVENT)

        # Act
        entry_view.handle_event(other_event)

        # Assert that the original event was passed to the component
        mock_handler.assert_called_once_with(other_event)


def test_entry_view_handle_event_mouse(entry_view: EntryView):
    """Tests that mouse events are translated and passed to child components."""
    # Spy on a real component's handle_event method
    mock_text_input = entry_view._text_input
    with patch.object(mock_text_input, "handle_event") as mock_handler:
        # Create a mouse event with screen-space coordinates
        # view is at (200, 200)
        mouse_event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, {"pos": (250, 250), "button": 1}
        )

        # Act
        entry_view.handle_event(mouse_event)

        # Assert
        mock_handler.assert_called_once()
        call_args, _ = mock_handler.call_args
        translated_event = call_args[0]
        # Expected position is (250-200, 250-200) = (50, 50)
        assert translated_event.pos == (50, 50)
        assert translated_event.type == pygame.MOUSEBUTTONDOWN
