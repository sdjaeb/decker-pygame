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


class _DummyFont:
    def __init__(self, *args, **kwargs):
        # Default line height used by many components
        self._linesize = 12

    def get_linesize(self) -> int:
        return self._linesize

    def size(self, _text: str) -> tuple[int, int]:
        return (1, 1)

    def render(self, *args, **kwargs) -> pygame.Surface:
        # Expected signature: render(text, antialias, color)
        color = None
        if len(args) >= 3:
            color = args[2]
        elif "color" in kwargs:
            color = kwargs["color"]
        if color is None:
            color = (0, 0, 0, 255)

        surf = pygame.Surface((1, 1), pygame.SRCALPHA)
        try:
            surf.fill(color)
        except Exception:
            surf.fill(tuple(color))
        return surf


@pytest.fixture(autouse=True)
def dummy_font(monkeypatch):
    """Monkeypatch pygame.font.Font and SysFont to a DummyFont for tests.

    The fixture is autouse so all tests automatically receive a stable
    font implementation without needing to initialize pygame's font
    subsystem. Tests that need the real font can re-initialize/override it
    locally.
    """
    monkeypatch.setattr(pygame.font, "Font", _DummyFont)
    monkeypatch.setattr(pygame.font, "SysFont", _DummyFont)
    yield
