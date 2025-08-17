"""Tests for the PercentageBar component."""

from collections.abc import Generator

import pygame
import pytest

from decker_pygame.presentation.components.percentage_bar import PercentageBar
from decker_pygame.settings import RED, WHITE


@pytest.fixture(autouse=True)
def pygame_init_fixture() -> Generator[None]:
    """Fixture to initialize pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


def test_percentage_bar_initialization() -> None:
    """Tests that the PercentageBar initializes correctly."""
    bar = PercentageBar(position=(10, 20), width=100, height=10, initial_color=RED)
    assert bar.rect.topleft == (10, 20)
    assert bar.rect.size == (100, 10)
    assert bar._percentage == 100.0
    assert bar._color == RED


def test_set_percentage() -> None:
    """Tests that set_percentage correctly sets and clamps the value."""
    bar = PercentageBar(position=(0, 0), width=100, height=10, initial_color=RED)

    # Test normal value
    bar.set_percentage(50.5)
    assert bar._percentage == 50.5

    # Test clamping above 100
    bar.set_percentage(120.0)
    assert bar._percentage == 100.0

    # Test clamping below 0
    bar.set_percentage(-10.0)
    assert bar._percentage == 0.0


def test_update_draws_correctly() -> None:
    """Tests that the update method draws the bar with the correct width."""
    bar = PercentageBar(position=(0, 0), width=200, height=10, initial_color=WHITE)

    bar.set_percentage(50)
    bar.update()
    # The bar should be filled up to half its width (100px).
    assert bar.image.get_at((99, 5)) == WHITE  # Inside the filled area
    assert bar.image.get_at((100, 5)) == pygame.Color(0, 0, 0, 0)
