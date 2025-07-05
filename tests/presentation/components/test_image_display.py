import pygame
import pytest

from decker_pygame.presentation.components.image_display import ImageDisplay


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


def test_initialization():
    """Tests that the ImageDisplay initializes with the correct image and position."""
    test_image = pygame.Surface((50, 60))
    test_image.fill((255, 0, 255))  # Fill with a distinct color

    display = ImageDisplay(position=(10, 20), image=test_image)

    assert isinstance(display, pygame.sprite.Sprite)
    assert display.image is test_image
    assert display.rect.topleft == (10, 20)
    assert display.rect.size == (50, 60)
