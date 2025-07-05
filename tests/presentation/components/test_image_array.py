import pygame
import pytest

from decker_pygame.presentation.components.image_array import ImageArray


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def image_list() -> list[pygame.Surface]:
    """Provides a list of mock surfaces for testing."""
    images = [pygame.Surface((10, 20)), pygame.Surface((30, 40))]
    images[0].fill((255, 0, 0))  # Red
    images[1].fill((0, 255, 0))  # Green
    return images


def test_initialization(image_list: list[pygame.Surface]):
    """Tests that the ImageArray initializes with the first image."""
    img_array = ImageArray(position=(50, 60), images=image_list)

    assert isinstance(img_array, pygame.sprite.Sprite)
    assert img_array.rect.topleft == (50, 60)
    assert img_array.image is image_list[0]
    assert img_array._current_index == 0


def test_initialization_with_no_images():
    """Tests that initializing with an empty list raises an error."""
    with pytest.raises(ValueError, match="at least one image"):
        ImageArray(position=(0, 0), images=[])


def test_set_image(image_list: list[pygame.Surface]):
    """Tests changing the displayed image with a valid index."""
    img_array = ImageArray(position=(50, 60), images=image_list)
    img_array.set_image(1)
    assert img_array.image is image_list[1]
    assert img_array._current_index == 1


def test_set_image_invalid_index(image_list: list[pygame.Surface], capsys):
    """Tests that an invalid index does not change the image and prints a warning."""
    img_array = ImageArray(position=(50, 60), images=image_list)

    img_array.set_image(99)
    assert img_array.image is image_list[0]  # Should not change
    assert "Warning: Invalid index 99" in capsys.readouterr().out
