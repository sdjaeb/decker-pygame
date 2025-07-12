from unittest.mock import Mock, patch

import pygame
import pytest

from decker_pygame.presentation.utils import get_and_ensure_rect, scale_icons

# --- Tests for scale_icons ---


def test_scale_icons():
    """
    Tests that the scale_icons utility correctly calls pygame.transform.scale
    for each icon in the list.
    """
    # Arrange
    icons = [pygame.Surface((16, 16)), pygame.Surface((16, 16))]
    target_size = (32, 32)

    with patch("decker_pygame.presentation.utils.pygame.transform.scale") as mock_scale:
        mock_scale.return_value = Mock(spec=pygame.Surface)

        # Act
        result = scale_icons(icons, target_size)

        # Assert
        assert mock_scale.call_count == 2
        mock_scale.assert_called_with(icons[1], target_size)
        assert len(result) == 2


def test_scale_icons_with_empty_list():
    """
    Tests that scale_icons handles an empty list gracefully without calling
    the scaling function. This covers the previously missed branch.
    """
    with patch("decker_pygame.presentation.utils.pygame.transform.scale") as mock_scale:
        result = scale_icons([], (32, 32))

        assert result == []
        mock_scale.assert_not_called()


# --- Tests for get_and_ensure_rect ---


def test_get_and_ensure_rect_with_existing_rect():
    """Tests that the function returns an existing rect."""
    sprite = pygame.sprite.Sprite()
    expected_rect = pygame.Rect(10, 10, 20, 20)
    sprite.rect = expected_rect

    rect = get_and_ensure_rect(sprite)
    assert rect is expected_rect


def test_get_and_ensure_rect_creates_from_image():
    """Tests that the function creates a rect from a sprite's image."""
    sprite = pygame.sprite.Sprite()
    sprite.image = pygame.Surface((50, 50))

    rect = get_and_ensure_rect(sprite)
    assert hasattr(sprite, "rect")
    assert rect.size == (50, 50)
    assert rect is sprite.rect


def test_get_and_ensure_rect_raises_error():
    """Tests that the function raises an error if no rect or image exists."""
    sprite = pygame.sprite.Sprite()  # Has no .rect or .image
    with pytest.raises(AttributeError, match="Cannot get rect"):
        get_and_ensure_rect(sprite)
