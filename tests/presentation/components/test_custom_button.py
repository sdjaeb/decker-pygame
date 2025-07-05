from unittest.mock import Mock

import pygame
import pytest

from decker_pygame.presentation.components.custom_button import CustomButton


@pytest.fixture
def button_assets():
    """Provides mock surfaces and a callback for button tests."""
    pygame.init()
    image_up = pygame.Surface((100, 50))
    image_down = pygame.Surface((100, 50))
    image_up.fill((100, 100, 100))
    image_down.fill((50, 50, 50))
    mock_callback = Mock()
    yield image_up, image_down, mock_callback
    pygame.quit()


def test_button_initialization(button_assets):
    """Tests that the button initializes with the correct state and image."""
    image_up, image_down, mock_callback = button_assets
    button = CustomButton((10, 20), image_up, image_down, mock_callback)

    assert button.rect.topleft == (10, 20)
    assert button.image is image_up  # Should start with the "up" image
    mock_callback.assert_not_called()


def test_button_successful_click(button_assets):
    """Tests a successful click: mouse down and up inside the button."""
    image_up, image_down, mock_callback = button_assets
    button = CustomButton((10, 20), image_up, image_down, mock_callback)

    # Simulate mouse down inside the button
    mouse_down_event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (15, 25)}
    )
    button.handle_event(mouse_down_event)
    assert button.image is image_down  # Image should change to "down"
    mock_callback.assert_not_called()

    # Simulate mouse up inside the button
    mouse_up_event = pygame.event.Event(
        pygame.MOUSEBUTTONUP, {"button": 1, "pos": (15, 25)}
    )
    button.handle_event(mouse_up_event)
    assert button.image is image_up  # Image should return to "up"
    mock_callback.assert_called_once()


def test_button_unsuccessful_click(button_assets):
    """Tests an unsuccessful click: mouse down inside, but up outside."""
    image_up, image_down, mock_callback = button_assets
    button = CustomButton((10, 20), image_up, image_down, mock_callback)

    # Simulate mouse down inside the button
    mouse_down_event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (15, 25)}
    )
    button.handle_event(mouse_down_event)
    assert button.image is image_down

    # Simulate mouse up OUTSIDE the button
    mouse_up_event = pygame.event.Event(
        pygame.MOUSEBUTTONUP, {"button": 1, "pos": (200, 200)}
    )
    button.handle_event(mouse_up_event)
    assert button.image is image_up  # Image should still return to "up"
    mock_callback.assert_not_called()  # Callback should NOT be called
