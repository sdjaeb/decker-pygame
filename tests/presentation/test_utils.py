import pygame
import pytest

from decker_pygame.presentation.utils import get_and_ensure_rect


@pytest.fixture(autouse=True)
def pygame_context():
    """Fixture to automatically initialize and quit Pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


def test_get_rect_from_existing_rect():
    """Tests that the function returns an existing rect."""
    sprite = pygame.sprite.Sprite()
    expected_rect = pygame.Rect(10, 20, 30, 40)
    sprite.rect = expected_rect

    rect = get_and_ensure_rect(sprite)
    assert rect is expected_rect


def test_get_rect_from_image():
    """Tests that the function creates and returns a rect from a sprite's image."""
    sprite = pygame.sprite.Sprite()
    sprite.image = pygame.Surface((50, 60))

    assert not hasattr(sprite, "rect") or sprite.rect is None
    rect = get_and_ensure_rect(sprite)
    assert hasattr(sprite, "rect")
    assert sprite.rect is rect
    assert rect.size == (50, 60)


def test_get_rect_fails_for_invalid_sprite():
    """Tests that the function raises an error for a sprite with no rect or image."""
    sprite = pygame.sprite.Sprite()  # A bare sprite

    with pytest.raises(AttributeError, match="Cannot get rect for sprite"):
        get_and_ensure_rect(sprite)


def test_get_rect_handles_none_attributes():
    """Tests that the function handles cases where attributes are explicitly None."""
    sprite_with_none_rect = pygame.sprite.Sprite()
    sprite_with_none_rect.rect = None
    sprite_with_none_rect.image = pygame.Surface((10, 10))

    rect = get_and_ensure_rect(sprite_with_none_rect)
    assert rect.size == (10, 10)
