"""Tests for the Slider component."""

from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.presentation.components.slider import Slider


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def on_change_mock() -> Mock:
    """Provides a mock for the on_change callback."""
    return Mock()


@pytest.fixture
def slider(on_change_mock: Mock) -> Slider:
    """Provides a Slider instance for testing."""
    return Slider(
        position=(10, 20),
        size=(100, 20),
        min_val=0,
        max_val=100,
        initial_val=50,
        on_change=on_change_mock,
    )


def test_slider_initialization(slider: Slider):
    """Tests that the slider initializes in the correct state."""
    assert slider.rect.topleft == (10, 20)
    assert slider.value == 50


def test_slider_drag_and_drop(slider: Slider, on_change_mock: Mock):
    """Tests that dragging the slider updates its value and calls the callback."""
    # Simulate mouse down on the slider
    # Slider is at (10, 20), so click at (10+1, 20+1)
    down_event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (11, 21)}
    )
    slider.handle_event(down_event)
    assert slider._dragging is True
    # The value should jump to the click position
    on_change_mock.assert_called_once()
    assert slider.value == pytest.approx(1.11, 0.01)

    # Simulate mouse motion while dragging
    # Move mouse to the 75% position of the slider (10 + 75 = 85)
    motion_event = pygame.event.Event(pygame.MOUSEMOTION, {"pos": (85, 21)})
    slider.handle_event(motion_event)
    assert slider.value == pytest.approx(75, 1)
    assert on_change_mock.call_count == 2

    # Simulate mouse up to stop dragging
    up_event = pygame.event.Event(pygame.MOUSEBUTTONUP, {"button": 1, "pos": (85, 21)})
    slider.handle_event(up_event)
    assert slider._dragging is False


def test_slider_value_clamping(slider: Slider):
    """Tests that the slider value is clamped to its min/max range."""
    # Try to drag beyond the max
    down_event = pygame.event.Event(
        pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (11, 21)}
    )
    slider.handle_event(down_event)
    motion_event = pygame.event.Event(pygame.MOUSEMOTION, {"pos": (200, 21)})
    slider.handle_event(motion_event)
    assert slider.value == 100

    # Try to drag before the min
    motion_event = pygame.event.Event(pygame.MOUSEMOTION, {"pos": (0, 21)})
    slider.handle_event(motion_event)
    assert slider.value == 0


def test_slider_update(slider: Slider):
    """Tests that the update method redraws the slider."""
    with patch("pygame.draw.rect") as mock_draw_rect:
        slider.update()
        # Should be called for the track and the handle
        assert mock_draw_rect.call_count == 2


def test_slider_update_zero_range(on_change_mock: Mock):
    """Tests that the update method handles a zero value range without errors."""
    zero_range_slider = Slider(
        position=(10, 20),
        size=(100, 20),
        min_val=50,
        max_val=50,
        initial_val=50,
        on_change=on_change_mock,
    )
    with patch("pygame.draw.rect") as mock_draw_rect:
        zero_range_slider.update()
        # Should still draw the track and handle
        assert mock_draw_rect.call_count == 2
