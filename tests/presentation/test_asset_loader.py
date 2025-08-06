import types
from pathlib import Path
from typing import Optional
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
    images = load_images("programs", base_path=asset_directory)
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
    load_images("programs", size=size, base_path=asset_directory)
    assert mock_pygame_image.transform.scale.call_count == 2  # Two images loaded
    mock_pygame_image.transform.scale.assert_called_with(
        mock_pygame_image.image.load.return_value, size
    )


def test_load_images_default_path(mocker: MockerFixture):
    """Test that load_images uses the default GFX.asset_folder."""
    mock_iterdir = mocker.patch("pathlib.Path.iterdir", return_value=[])
    mocker.patch("pygame.image.load")

    # Call without base_path to test the default path logic
    load_images("programs")

    # Assert that the default path logic was triggered
    mock_iterdir.assert_called_once()


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
    mock_sheet.convert.return_value = mock_sheet
    mocker.patch("pygame.image.load", return_value=mock_sheet)

    # Mock the Surface class to intercept the creation of new sprite surfaces
    mock_surface_instance = MagicMock(spec=pygame.Surface)
    mock_surface_class = mocker.patch(
        "decker_pygame.presentation.asset_loader.pygame.Surface",
        return_value=mock_surface_instance,
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
    assert all(s is mock_surface_instance for s in sprites)
    assert dimensions == (sheet_width, sheet_height)
    mock_surface_class.assert_has_calls([call((32, 32)), call((32, 32))])
    mock_surface_instance.blit.assert_has_calls(
        [
            call(mock_sheet, (0, 0), pygame.Rect(0, 0, 32, 32)),
            call(mock_sheet, (0, 0), pygame.Rect(32, 0, 32, 32)),
        ]
    )
    if expect_colorkey_call:
        assert mock_surface_instance.set_colorkey.call_count == 2
        mock_surface_instance.set_colorkey.assert_called_with(colorkey)
    else:
        mock_surface_instance.set_colorkey.assert_not_called()
