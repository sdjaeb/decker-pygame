import pygame
import pytest

from decker_pygame.presentation.components.health_bar import HealthBar
from decker_pygame.settings import HEALTH


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def health_bar():
    """Provides a HealthBar instance for testing."""
    return HealthBar(position=(10, 10), width=100, height=10)


def test_initialization(health_bar: HealthBar):
    """Tests that the health bar initializes to a full, green state."""
    assert health_bar.rect.topleft == (10, 10)
    assert health_bar._health_percent == 100
    assert health_bar._color == HEALTH.colors[0][1]  # Green


@pytest.mark.parametrize(
    "current, maximum, expected_percent, expected_color_index",
    [
        (100, 100, 100, 0),  # Full health -> Green
        (40, 80, 50, 1),  # Half health -> Yellow
        (10, 100, 10, 2),  # Low health -> Red
        (0, 100, 0, 2),  # Zero health -> Red
        (120, 100, 100, 0),  # Over-full health -> Green (clamped)
        (-10, 100, 0, 2),  # Negative health -> Red (clamped)
        (50, 0, 0, 2),  # Zero max health -> Red
    ],
)
def test_update_health(
    health_bar: HealthBar,
    current: int,
    maximum: int,
    expected_percent: float,
    expected_color_index: int,
):
    """Tests that the health bar updates its state and color correctly."""
    health_bar.update_health(current, maximum)

    assert health_bar._health_percent == pytest.approx(expected_percent)
    assert health_bar._color == HEALTH.colors[expected_color_index][1]

    # Check that the bar is drawn with the correct width
    drawn_width = health_bar.image.get_bounding_rect().width
    expected_width = int(100 * (expected_percent / 100))
    assert drawn_width == expected_width
