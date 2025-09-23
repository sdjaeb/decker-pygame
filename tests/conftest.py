"""Global fixtures for the test suite."""

from collections.abc import Generator
from os import environ

import pygame
import pytest


@pytest.fixture(scope="session", autouse=True)
def pygame_session() -> Generator[None]:
    """Initializes pygame for the test session to enable surface conversions."""
    environ["SDL_VIDEODRIVER"] = "dummy"
    # Set a dummy display mode to allow for surface conversions
    pygame.display.set_mode((1, 1))
    pygame.init()
    yield
    pygame.quit()
