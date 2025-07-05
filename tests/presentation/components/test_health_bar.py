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
def health_bar_instance() -> HealthBar:
    """Provides a default HealthBar instance for tests."""
    return HealthBar(position=(10, 20), width=200, height=20)


def test_initialization(health_bar_instance: HealthBar):
    """Tests that the health bar initializes correctly."""
    bar = health_bar_instance
    assert isinstance(bar, pygame.sprite.Sprite)
    assert bar.rect.topleft == (10, 20)
    assert bar._percentage == 100.0
    assert bar._color == HEALTH.colors[0][1]  # Full health color


@pytest.mark.parametrize(
    "current, maximum, expected_percent, expected_color_index",
    [
        (100, 100, 100.0, 0),  # Full health -> Green
        (40, 100, 40.0, 1),  # Mid health -> Yellow
        (10, 100, 10.0, 2),  # Low health -> Red
        (0, 100, 0.0, 2),  # Zero health -> Red
        (120, 100, 100.0, 0),  # Clamped high
        (-10, 100, 0.0, 2),  # Clamped low
    ],
)
def test_update_health(
    health_bar_instance: HealthBar,
    current: int,
    maximum: int,
    expected_percent: float,
    expected_color_index: int,
):
    """Tests updating health and color based on different values."""
    bar = health_bar_instance
    bar.update_health(current, maximum)
    assert bar._percentage == expected_percent
    assert bar._color == HEALTH.colors[expected_color_index][1]
