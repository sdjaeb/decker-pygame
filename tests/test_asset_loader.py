import types
from pathlib import Path
from unittest.mock import MagicMock, call

import pygame
import pytest
from decker_pygame.asset_loader import load_images
from pytest_mock import MockerFixture


@pytest.fixture
def mock_pygame_image(mocker: MockerFixture) -> types.ModuleType:
    """Fixture to mock pygame.image.load and transform."""
    mock_surface = MagicMock(spec=pygame.Surface)
    mock_surface.convert_alpha.return_value = mock_surface
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


def test_load_images_no_resize(
    mock_pygame_image: types.ModuleType, asset_directory: Path
):
    """Test loading images without resizing, ensuring correct order and filtering."""
    images = load_images("programs", base_path=asset_directory)
    assert len(images) == 2
    expected_calls = [
        call(str(asset_directory / "programs" / "prog_a.png")),
        call(str(asset_directory / "programs" / "prog_b.png")),
    ]
    mock_pygame_image.image.load.assert_has_calls(expected_calls)
    mock_pygame_image.transform.scale.assert_not_called()


def test_load_images_with_resize(
    mock_pygame_image: types.ModuleType, asset_directory: Path
):
    """Test loading images with resizing."""
    size = (32, 32)
    images = load_images("programs", size=size, base_path=asset_directory)
    assert len(images) == 2
    assert mock_pygame_image.transform.scale.call_count == 2
    mock_pygame_image.transform.scale.assert_called_with(pygame.image.load(), size)


def test_load_images_uses_default_path(
    mock_pygame_image: types.ModuleType, mocker: MockerFixture
):
    """Test load_images uses the default GFX.asset_folder when no base_path is given."""
    # Mock the file system interaction to avoid needing real files
    mock_iterdir = mocker.patch("pathlib.Path.iterdir", return_value=[])

    # This call will execute the line under test
    load_images("programs")

    # The test passes if no exception is raised and we can assert the mock was called
    mock_iterdir.assert_called_once()
