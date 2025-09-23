import types
from pathlib import Path
from typing import Optional, cast
from unittest.mock import MagicMock, call

import pygame
import pytest
from pytest_mock import MockerFixture

from decker_pygame.presentation.asset_loader import load_images, load_spritesheet


@pytest.fixture
def mock_pygame_image(mocker: MockerFixture) -> types.ModuleType:
    """Fixture to mock pygame.image.load and transform."""
    mock_surface = MagicMock(spec=pygame.Surface)
    mock_surface.convert_alpha.return_value = mock_surface
    mock_surface.convert.return_value = mock_surface
    mocker.patch("pygame.image.load", return_value=mock_surface)
    mocker.patch("pygame.transform.scale", return_value=mock_surface)
    return pygame


@pytest.fixture
def asset_directory(tmp_path: Path) -> Path:
    """Create a temporary asset directory structure for testing."""
    programs_path = tmp_path / "programs"
    programs_path.mkdir()
    (programs_path / "prog_b.png").touch()
    (programs_path / "prog_a.png").touch()
    (programs_path / "readme.txt").touch()  # Should be ignored
    return tmp_path


def test_load_images(mock_pygame_image: types.ModuleType, asset_directory: Path):
    """Test loading images from a directory, ensuring correct order and filtering."""
    images = load_images(base_path=asset_directory, subdirectory="programs")
    assert len(images) == 2
    expected_calls = [
        call(str(asset_directory / "programs" / "prog_a.png")),
        call(str(asset_directory / "programs" / "prog_b.png")),
    ]
    mock_pygame_image.image.load.assert_has_calls(expected_calls)


def test_load_images_with_resize(
    mock_pygame_image: types.ModuleType, asset_directory: Path
):
    """Test loading images with resizing."""
    size = (64, 64)
    load_images(base_path=asset_directory, subdirectory="programs", size=size)
    assert mock_pygame_image.transform.scale.call_count == 2  # Two images loaded
    mock_pygame_image.transform.scale.assert_called_with(
        mock_pygame_image.image.load.return_value, size
    )


@pytest.mark.parametrize(
    "colorkey, expect_colorkey_call",
    [
        (None, False),
        ((0, 0, 0), True),
    ],
)
def test_load_spritesheet(
    mocker: MockerFixture, colorkey: Optional[tuple], expect_colorkey_call: bool
):
    """Test loading and slicing a spritesheet with and without a colorkey."""
    # 1. Arrange
    sheet_width, sheet_height = 64, 32  # 2x1 grid of 32x32 sprites
    sprite_width, sprite_height = 32, 32

    # Mock the main sheet loaded from disk
    mock_sheet = MagicMock(spec=pygame.Surface)
    mock_sheet.get_size.return_value = (sheet_width, sheet_height)
    # The function uses convert_alpha(), so we must mock that.
    mock_sheet.convert_alpha.return_value = mock_sheet
    mocker.patch("pygame.image.load", return_value=mock_sheet)

    # Mock the Surface class to intercept the creation of new sprite surfaces
    # The side_effect ensures a new mock is created for each sprite.
    mock_surface_class = mocker.patch(
        "decker_pygame.presentation.asset_loader.pygame.Surface",
        side_effect=[MagicMock(spec=pygame.Surface, autospec=True) for _ in range(2)],
    )

    # 2. Act
    sprites, dimensions = load_spritesheet(
        "dummy_sheet.bmp",
        sprite_width,
        sprite_height,
        colorkey=colorkey,
        base_path=Path("/fake/path"),
    )

    # 3. Assert
    assert len(sprites) == 2
    # Check that two distinct mock surfaces were created and returned
    assert sprites[0] is not sprites[1]
    assert dimensions == (sheet_width, sheet_height)

    # Check that the Surface constructor was called correctly for each sprite
    mock_surface_class.assert_has_calls(
        [call((32, 32), pygame.SRCALPHA), call((32, 32), pygame.SRCALPHA)]
    )
    # Check that blit was called on each of the created sprite surfaces
    cast(MagicMock, sprites[0].blit).assert_called_once_with(
        mock_sheet, (0, 0), pygame.Rect(0, 0, 32, 32)
    )
    cast(MagicMock, sprites[1].blit).assert_called_once_with(
        mock_sheet, (0, 0), pygame.Rect(32, 0, 32, 32)
    )
    if expect_colorkey_call:
        cast(MagicMock, sprites[0].set_colorkey).assert_called_once_with(colorkey)
        cast(MagicMock, sprites[1].set_colorkey).assert_called_once_with(colorkey)
    else:
        cast(MagicMock, sprites[0].set_colorkey).assert_not_called()
        cast(MagicMock, sprites[1].set_colorkey).assert_not_called()
