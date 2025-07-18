"""Tests for the Checkbox component."""

from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.presentation.components.checkbox import Checkbox


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def on_toggle_mock() -> Mock:
    """Provides a mock for the on_toggle callback."""
    return Mock()


@pytest.fixture
def checkbox(on_toggle_mock: Mock) -> Checkbox:
    """Provides a Checkbox instance for testing."""
    # We need to patch the Font constructor to return a mock instance
    # that we can control, specifically its render method.
    with patch("pygame.font.Font") as mock_font_class:
        mock_font_instance = Mock()
        mock_font_instance.render.return_value = pygame.Surface((50, 16))
        mock_font_class.return_value = mock_font_instance
        yield Checkbox(position=(10, 20), label="Test", on_toggle=on_toggle_mock)


def test_checkbox_initialization(checkbox: Checkbox):
    """Tests that the checkbox initializes in the correct state."""
    assert checkbox.rect.topleft == (10, 20)
    assert checkbox.is_checked is False


def test_checkbox_toggle_state(checkbox: Checkbox, on_toggle_mock: Mock):
    """Tests that the internal toggle logic works correctly."""
    # Initial state is False
    assert checkbox.is_checked is False

    # First toggle
    checkbox._on_click()
    assert checkbox.is_checked is True
    on_toggle_mock.assert_called_once_with(True)

    # Second toggle
    checkbox._on_click()
    assert checkbox.is_checked is False
    on_toggle_mock.assert_called_with(False)
    assert on_toggle_mock.call_count == 2


def test_checkbox_handle_event(checkbox: Checkbox):
    """Tests that handle_event correctly triggers the toggle."""
    with patch.object(checkbox, "_on_click") as mock_on_click:
        # Click inside
        event_inside = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": checkbox.rect.center}
        )
        checkbox.handle_event(event_inside)
        mock_on_click.assert_called_once()

        # Click outside
        event_outside = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, {"button": 1, "pos": (0, 0)}
        )
        checkbox.handle_event(event_outside)
        # Should not be called again
        mock_on_click.assert_called_once()


def test_checkbox_update_draws_checkmark(checkbox: Checkbox):
    """Tests that the update method draws the checkmark when checked."""
    with patch("pygame.draw.line") as mock_draw_line:
        checkbox.is_checked = True
        checkbox.update()
        assert mock_draw_line.call_count == 2

        checkbox.is_checked = False
        checkbox.update()
        # Should not have been called again
        assert mock_draw_line.call_count == 2
