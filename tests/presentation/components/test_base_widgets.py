from unittest.mock import Mock

import pygame
import pytest

from decker_pygame.presentation.components.base_widgets import Clickable


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


class ConcreteClickable(Clickable):
    """A concrete implementation of the abstract Clickable for testing."""

    def __init__(self, on_click: Mock):
        """Initialize the concrete clickable."""
        super().__init__(on_click)
        # Provide a dummy rect required by the Sprite base class
        self.rect = pygame.Rect(0, 0, 10, 10)

    def handle_event(self, event: pygame.event.Event) -> None:
        """A minimal implementation of the abstract method for testing."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._on_click()


def test_clickable_initialization():
    """Tests that the Clickable abstract base class's __init__ works."""
    mock_callback = Mock()
    # We test the ABC's logic through a minimal concrete implementation
    instance = ConcreteClickable(on_click=mock_callback)
    assert instance._on_click is mock_callback


def test_cannot_instantiate_abstract_class():
    """Tests that the abstract Clickable class cannot be instantiated directly."""
    with pytest.raises(TypeError, match="Can't instantiate abstract class"):
        Clickable(on_click=Mock())  # type: ignore
