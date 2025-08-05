from unittest.mock import Mock

import pygame
import pytest

from decker_pygame.presentation.components.button import Button
from decker_pygame.settings import UI_FONT_DISABLED


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


def test_button_initialization():
    """Tests that the Button initializes and renders correctly."""
    mock_callback = Mock()
    button = Button(
        position=(10, 20),
        size=(100, 50),
        text="Click Me",
        on_click=mock_callback,
    )

    assert button.rect.topleft == (10, 20)
    assert button.rect.size == (100, 50)
    assert button.text == "Click Me"
    assert not button._is_pressed


def test_button_click_handler_outside():
    """Tests that clicking outside the button does not trigger the callback."""
    mock_callback = Mock()
    button = Button(
        position=(100, 100), size=(100, 50), text="Click", on_click=mock_callback
    )

    # Click is far away from the button
    click_pos = (300, 300)
    down_event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": click_pos}
    )
    up_event = pygame.event.Event(pygame.MOUSEBUTTONUP, {"button": 1, "pos": click_pos})

    button.handle_event(down_event)
    assert not button._is_pressed
    button.handle_event(up_event)
    mock_callback.assert_not_called()


def test_button_press_and_release_triggers_click():
    """Tests a full press and release cycle over the button triggers the callback."""
    mock_callback = Mock()
    button = Button(
        position=(100, 100), size=(100, 50), text="Click", on_click=mock_callback
    )

    # Press down over the button
    down_event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": button.rect.center}
    )
    button.handle_event(down_event)

    # Assert visual state changed and callback was not yet called
    assert button._is_pressed is True
    mock_callback.assert_not_called()

    # Release mouse over the button
    up_event = pygame.event.Event(
        pygame.MOUSEBUTTONUP, {"button": 1, "pos": button.rect.center}
    )
    button.handle_event(up_event)

    # Assert visual state reset and callback was called
    assert button._is_pressed is False
    mock_callback.assert_called_once()


def test_button_press_and_release_off_button_does_not_trigger():
    """Tests pressing on the button and releasing off does not trigger the callback."""
    mock_callback = Mock()
    button = Button(
        position=(100, 100), size=(100, 50), text="Click", on_click=mock_callback
    )

    # Press down over the button
    down_event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": button.rect.center}
    )
    button.handle_event(down_event)
    assert button._is_pressed is True

    # Release mouse off the button
    up_event = pygame.event.Event(
        pygame.MOUSEBUTTONUP, {"button": 1, "pos": (300, 300)}
    )
    button.handle_event(up_event)

    # Assert callback was not called
    assert not button._is_pressed
    mock_callback.assert_not_called()


def test_transparent_button_renders_no_background():
    """Tests that a transparent button does not draw a background."""
    mock_callback = Mock()
    button = Button(
        position=(10, 20),
        size=(100, 50),
        text="Transparent",
        on_click=mock_callback,
        is_transparent=True,
    )

    # The background should be fully transparent (alpha=0)
    # We check a corner pixel to be sure.
    assert button.image.get_at((0, 0)).a == 0


def test_disabled_button_does_not_handle_events():
    """Tests that a disabled button does not handle any mouse events."""
    mock_callback = Mock()
    button = Button(
        position=(100, 100), size=(100, 50), text="Click", on_click=mock_callback
    )
    button.set_enabled(False)  # Disable the button

    # Simulate a click
    down_event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": button.rect.center}
    )
    button.handle_event(down_event)

    up_event = pygame.event.Event(
        pygame.MOUSEBUTTONUP, {"button": 1, "pos": button.rect.center}
    )
    button.handle_event(up_event)

    mock_callback.assert_not_called()
    assert button._is_pressed is False  # Should remain false


def test_disabled_button_renders_correctly():
    """Tests that a disabled button renders with the correct text color."""
    mock_callback = Mock()
    button = Button(
        position=(10, 20),
        size=(100, 50),
        text="Disabled",
        on_click=mock_callback,
        is_transparent=True,  # Make button transparent for easier color checking
    )
    button.set_enabled(False)

    # Re-render the button to apply the disabled state visual
    button._render()

    # Get the color of a pixel where the text should be
    # This assumes the text is rendered in the center. Adjust if necessary.
    text_x, text_y = button.image.get_rect().center
    # Find a pixel that is not the background color (0,0,0,0 for transparent)
    # Iterate a small area around the center to find a non-transparent pixel
    found_color = None
    for x_offset in range(-5, 6):
        for y_offset in range(-5, 6):
            try:
                pixel_color = button.image.get_at(
                    (text_x + x_offset, text_y + y_offset)
                )
                if pixel_color.a != 0:  # Check for non-transparent pixel
                    found_color = pixel_color
                    break
            except IndexError:  # Handle cases where offset goes out of bounds
                continue
        if found_color:
            break

    assert found_color is not None, (
        "No non-transparent pixel found, text might not be rendered."
    )
    # Compare the RGB values, ignoring alpha
    assert found_color.r == UI_FONT_DISABLED.r
    assert found_color.g == UI_FONT_DISABLED.g
    assert found_color.b == UI_FONT_DISABLED.b
