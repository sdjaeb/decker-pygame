"""This file contains shared fixtures for the test suite."""

from collections.abc import Generator

import pygame
import pytest


@pytest.fixture(autouse=True)
def pygame_context() -> Generator[None]:
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    # Many pygame operations require a display to be set.
    pygame.display.set_mode((1, 1))
    yield
    pygame.quit()
