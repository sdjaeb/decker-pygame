import pygame
import pytest

from decker_pygame.presentation.components.node_view import NodeView


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def image_list() -> list[pygame.Surface]:
    """Provides a list of mock surfaces for testing."""
    images = [pygame.Surface((10, 10)), pygame.Surface((10, 10))]
    images[0].fill((0, 0, 255))  # Blue for 'normal'
    images[1].fill((255, 0, 0))  # Red for 'targeted'
    return images


def test_initialization(image_list: list[pygame.Surface]):
    """Tests that the NodeView initializes with the first image/state."""
    node_view = NodeView(position=(50, 60), images=image_list)

    assert isinstance(node_view, pygame.sprite.Sprite)
    assert node_view.rect.topleft == (50, 60)
    assert node_view.image is image_list[0]
    assert node_view._current_index == 0


def test_initialization_with_no_images():
    """Tests that initializing with an empty list raises an error."""
    with pytest.raises(ValueError, match="at least one image"):
        NodeView(position=(0, 0), images=[])


def test_set_state(image_list: list[pygame.Surface]):
    """Tests changing the displayed state with a valid index."""
    node_view = NodeView(position=(50, 60), images=image_list)
    node_view.set_state(1)
    assert node_view.image is image_list[1]
    assert node_view._current_index == 1


def test_set_state_invalid_index(image_list: list[pygame.Surface], capsys):
    """Tests that an invalid index does not change the state and prints a warning."""
    node_view = NodeView(position=(50, 60), images=image_list)

    node_view.set_state(99)
    assert node_view.image is image_list[0]  # Should not change
    assert "Warning: Invalid state_index 99" in capsys.readouterr().out
