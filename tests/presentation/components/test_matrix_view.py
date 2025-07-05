import pygame
import pytest

from decker_pygame.presentation.components.image_display import ImageDisplay
from decker_pygame.presentation.components.matrix_view import MatrixView


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


def test_matrix_view_initialization():
    """Tests that the MatrixView initializes with a background."""
    bg_color = pygame.Color("blue")
    view = MatrixView(position=(10, 20), size=(200, 150), background_color=bg_color)

    assert view.rect.topleft == (10, 20)
    assert view.rect.size == (200, 150)
    assert view.image.get_at((5, 5)) == bg_color


def test_matrix_view_add_component():
    """Tests that a component can be added and is drawn onto the view."""
    bg_color = pygame.Color("blue")
    child_color = pygame.Color("red")
    view = MatrixView(position=(0, 0), size=(200, 150), background_color=bg_color)

    # Create a simple child component to add
    child_image = pygame.Surface((50, 40))
    child_image.fill(child_color)
    child_component = ImageDisplay(position=(0, 0), image=child_image)

    # Add the component at a relative position
    view.add_component(child_component, relative_pos=(30, 20))

    # Check that the child's rect was updated to be relative to the view
    assert child_component.rect.topleft == (30, 20)

    # Check that the view's surface has been updated
    assert view.image.get_at((35, 25)) == child_color  # Inside child
    assert view.image.get_at((1, 1)) == bg_color  # Outside child
