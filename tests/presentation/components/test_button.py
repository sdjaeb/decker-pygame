from unittest.mock import Mock

import pygame
import pytest

from decker_pygame.presentation.components.button import Button


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
    button.handle_event(up_event)
    mock_callback.assert_not_called()


def test_button_press_and_release_triggers_click():
    """Tests a full press and release cycle over the button triggers the callback."""
    mock_callback = Mock()
    button = Button(
        position=(100, 100), size=(100, 50), text="Click", on_click=mock_callback
    )
    image_up = button.image

    # Press down over the button
    down_event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": button.rect.center}
    )
    button.handle_event(down_event)

    # Assert visual state changed and callback was not yet called
    assert button._is_pressed is True
    assert button.image is not image_up
    mock_callback.assert_not_called()

    # Release mouse over the button
    up_event = pygame.event.Event(
        pygame.MOUSEBUTTONUP, {"button": 1, "pos": button.rect.center}
    )
    button.handle_event(up_event)

    # Assert visual state reset and callback was called
    assert button._is_pressed is False
    assert button.image is image_up
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
    mock_callback.assert_not_called()
