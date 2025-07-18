"""Tests for the OptionsView component."""

from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.application.dtos import OptionsViewDTO
from decker_pygame.presentation.components.button import Button
from decker_pygame.presentation.components.checkbox import Checkbox
from decker_pygame.presentation.components.options_view import OptionsView


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
        "on_save": Mock(),
        "on_load": Mock(),
        "on_quit": Mock(),
        "on_close": Mock(),
        "on_toggle_sound": Mock(),
        "on_toggle_tooltips": Mock(),
    }


@pytest.fixture
def options_view_data() -> OptionsViewDTO:
    """Provides sample data for the OptionsView."""
    return OptionsViewDTO(sound_enabled=True, tooltips_enabled=False)


@pytest.fixture
def options_view(
    options_view_data: OptionsViewDTO, mock_callbacks: dict[str, Mock]
) -> OptionsView:
    """Provides an OptionsView instance for testing."""
    return OptionsView(
        data=options_view_data,
        on_save=mock_callbacks["on_save"],
        on_load=mock_callbacks["on_load"],
        on_quit=mock_callbacks["on_quit"],
        on_close=mock_callbacks["on_close"],
        on_toggle_sound=mock_callbacks["on_toggle_sound"],
        on_toggle_tooltips=mock_callbacks["on_toggle_tooltips"],
    )


def test_options_view_initialization(options_view: OptionsView):
    """Tests that the view is initialized correctly."""
    assert options_view.rect.topleft == (200, 200)
    # 1 title, 2 checkboxes, 4 buttons
    assert len(options_view._components) == 7

    sound_checkbox = next(
        c
        for c in options_view._components
        if isinstance(c, Checkbox) and c._label == "Sound Enabled"
    )
    tooltips_checkbox = next(
        c
        for c in options_view._components
        if isinstance(c, Checkbox) and c._label == "Tooltips Enabled"
    )

    assert sound_checkbox.is_checked is True
    assert tooltips_checkbox.is_checked is False


def test_button_callbacks(options_view: OptionsView, mock_callbacks: dict[str, Mock]):
    """Tests that clicking the buttons triggers the correct callbacks."""
    buttons = {c.text: c for c in options_view._components if isinstance(c, Button)}

    buttons["Save Game"]._on_click()
    mock_callbacks["on_save"].assert_called_once()

    buttons["Load Game"]._on_click()
    mock_callbacks["on_load"].assert_called_once()

    buttons["Quit to Main Menu"]._on_click()
    mock_callbacks["on_quit"].assert_called_once()

    buttons["Close"]._on_click()
    mock_callbacks["on_close"].assert_called_once()


def test_checkbox_callbacks(options_view: OptionsView, mock_callbacks: dict[str, Mock]):
    """Tests that toggling the checkboxes triggers the correct callbacks."""
    sound_checkbox = next(
        c
        for c in options_view._components
        if isinstance(c, Checkbox) and c._label == "Sound Enabled"
    )
    tooltips_checkbox = next(
        c
        for c in options_view._components
        if isinstance(c, Checkbox) and c._label == "Tooltips Enabled"
    )

    # Toggle sound (was True, becomes False)
    sound_checkbox._on_click()
    mock_callbacks["on_toggle_sound"].assert_called_once_with(False)

    # Toggle tooltips (was False, becomes True)
    tooltips_checkbox._on_click()
    mock_callbacks["on_toggle_tooltips"].assert_called_once_with(True)


def test_options_view_handle_event_mouse(options_view: OptionsView):
    """Tests that mouse events are translated and passed to child components."""
    # Spy on a real component's handle_event method
    mock_button = next(
        c
        for c in options_view._components
        if isinstance(c, Button) and c.text == "Close"
    )
    with patch.object(mock_button, "handle_event") as mock_handler:
        # Create a mouse event with screen-space coordinates
        # view is at (200, 200)
        mouse_event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, {"pos": (250, 250), "button": 1}
        )

        # Act
        options_view.handle_event(mouse_event)

        # Assert
        mock_handler.assert_called_once()
        call_args, _ = mock_handler.call_args
        translated_event = call_args[0]
        # Expected position is (250-200, 250-200) = (50, 50)
        assert translated_event.pos == (50, 50)


def test_options_view_update(options_view: OptionsView):
    """Tests that the update method calls update on its children."""
    # Add a mock component to spy on
    mock_component = Mock(spec=pygame.sprite.Sprite)
    # The mock needs 'image' and 'rect' attributes for the draw() call to work.
    mock_component.image = pygame.Surface((1, 1))
    mock_component.rect = pygame.Rect(0, 0, 1, 1)
    options_view._components.add(mock_component)

    # Call the update method
    options_view.update()

    # Assert that the mock component's update method was called
    mock_component.update.assert_called_once()
