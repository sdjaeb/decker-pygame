import types
from pathlib import Path
from unittest.mock import MagicMock, call

import pygame
import pytest
from decker_pygame.asset_loader import load_images, load_spritesheet
from pytest_mock import MockerFixture


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
    assert mock_pygame_image.transform.scale.call_count == 2
    mock_pygame_image.transform.scale.assert_called_with(pygame.image.load(), size)


def test_load_images_default_path(mocker: MockerFixture):
    """Test that load_images uses the default GFX.asset_folder."""
    mocker.patch("pathlib.Path.iterdir", return_value=[])
    mocker.patch("pygame.image.load")

    # Call without base_path to test the default path logic
    load_images("programs")


def test_load_spritesheet(mocker: MockerFixture):
    """Test loading and slicing a spritesheet with a colorkey."""
    # 1. Mock dependencies
    sheet_width, sheet_height = 64, 32  # 2x1 grid of 32x32 sprites
    sprite_width, sprite_height = 32, 32
    mock_sheet_surface = MagicMock(spec=pygame.Surface)
    mock_sheet_surface.get_size.return_value = (sheet_width, sheet_height)
    mock_sheet_surface.convert.return_value = mock_sheet_surface
    mocker.patch("pygame.image.load", return_value=mock_sheet_surface)

    # Mock the Surface class to inspect instances created by the function
    mock_surface_instance = MagicMock(spec=pygame.Surface)
    mock_surface_class = mocker.patch(
        "pygame.Surface", return_value=mock_surface_instance
    )

    # 2. Call the function under test
    sprites, dimensions = load_spritesheet(
        "dummy_sheet.bmp",
        sprite_width=sprite_width,
        sprite_height=sprite_height,
        colorkey=(0, 0, 0),
        base_path=Path("/fake/path"),
    )

    # 3. Assert results
    assert len(sprites) == 2
    assert dimensions == (sheet_width, sheet_height)
    mock_surface_class.assert_has_calls([call((32, 32)), call((32, 32))])
    mock_surface_instance.blit.assert_has_calls(
        [
            call(mock_sheet_surface, (0, 0), pygame.Rect(0, 0, 32, 32)),
            call(mock_sheet_surface, (0, 0), pygame.Rect(32, 0, 32, 32)),
        ]
    )
    assert mock_surface_instance.set_colorkey.call_count == 2
    mock_surface_instance.set_colorkey.assert_called_with((0, 0, 0))


def test_load_spritesheet_default_path(mocker: MockerFixture):
    """Test that load_spritesheet uses the default GFX.asset_folder."""
    mock_sheet_surface = MagicMock(spec=pygame.Surface)
    mock_sheet_surface.get_size.return_value = (0, 0)  # Prevents loops
    mock_sheet_surface.convert.return_value = mock_sheet_surface
    mock_load = mocker.patch("pygame.image.load", return_value=mock_sheet_surface)

    # Call without base_path to test the default path logic
    load_spritesheet("dummy.bmp", 16, 16)

    # Assert that the load was attempted. The path will be constructed from
    # GFX.asset_folder which is a real path, so we just check that the call
    # happened with a string path.
    mock_load.assert_called_once()
    assert isinstance(mock_load.call_args[0][0], str)
