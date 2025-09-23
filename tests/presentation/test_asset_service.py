"""Tests for the AssetService."""

import json
from collections.abc import Generator
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pygame
import pytest

from decker_pygame.presentation.asset_service import AssetService


@pytest.fixture
def temp_asset_dir() -> Generator[str]:
    """Create a temporary directory for test asset files."""
    with TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def assets_config_file(temp_asset_dir: str) -> Path:
    """Create a temporary assets.json file and return its path."""
    config_path = Path(temp_asset_dir) / "assets.json"
    return config_path


def test_asset_service_loads_images_and_spritesheets(
    assets_config_file: Path, temp_asset_dir: str
):
    """Tests that the AssetService correctly loads all asset types."""
    # Create dummy asset files in a subdirectory for image loading
    image_dir = Path(temp_asset_dir) / "icons"
    image_dir.mkdir()
    dummy_image_path = image_dir / "dummy.bmp"
    pygame.image.save(pygame.Surface((10, 10)), str(dummy_image_path))

    dummy_sheet_path = Path(temp_asset_dir) / "sheet.bmp"
    pygame.image.save(pygame.Surface((32, 16)), str(dummy_sheet_path))

    # Create the assets.json content
    config_data = {
        # The service now loads from a directory
        "images": {"dummy_image": {"dir": "icons"}},
        "spritesheets": {
            "dummy_sheet": {
                "file": "sheet.bmp",
                "sprite_width": 16,
                "sprite_height": 16,
                "colorkey": [255, 0, 255],
            }
        },
    }
    with open(assets_config_file, "w") as f:
        json.dump(config_data, f)

    # Patch GFX.asset_folder to point to our temp directory
    with patch(
        "decker_pygame.presentation.asset_service.GFX.asset_folder",
        Path(temp_asset_dir),
    ):
        service = AssetService(assets_config_path=assets_config_file)

        # Test image loading
        image = service.get_image("dummy_image")
        assert image is not None
        assert isinstance(image, pygame.Surface)
        assert image.get_size() == (10, 10)

        # Test spritesheet loading
        sheet = service.get_spritesheet("dummy_sheet")
        assert sheet is not None
        assert len(sheet) == 2
        assert all(isinstance(s, pygame.Surface) for s in sheet)


def test_get_non_existent_image(assets_config_file: Path):
    """Tests that getting a non-existent image returns None."""
    with open(assets_config_file, "w") as f:
        json.dump({"images": {}, "spritesheets": {}}, f)

    service = AssetService(assets_config_path=assets_config_file)
    image = service.get_image("non_existent")

    assert image is None


def test_get_non_existent_spritesheet(assets_config_file: Path):
    """Tests that getting a non-existent spritesheet returns an empty list."""
    with open(assets_config_file, "w") as f:
        json.dump({"images": {}, "spritesheets": {}}, f)

    service = AssetService(assets_config_path=assets_config_file)
    sheet = service.get_spritesheet("non_existent")

    assert sheet == []


def test_asset_service_handles_load_error(
    assets_config_file: Path, temp_asset_dir: str
):
    """Tests that the AssetService handles a pygame.error on load."""
    # Create a config that points to a non-existent directory
    config_data = {"images": {"bad_image": {"dir": "non_existent_dir"}}}
    with open(assets_config_file, "w") as f:
        json.dump(config_data, f)

    # Patch GFX.asset_folder. The error will be raised when iterdir() is called
    # on a path that doesn't exist. The service should catch this.
    with patch(
        "decker_pygame.presentation.asset_service.GFX.asset_folder",
        Path(temp_asset_dir),
    ):
        # The service should catch the error and continue
        service = AssetService(assets_config_path=assets_config_file)

        # The bad image should not be in the loaded assets
        image = service.get_image("bad_image")
        assert image is None


def test_asset_service_handles_file_not_found(
    assets_config_file: Path, temp_asset_dir: str, capsys
):
    """Tests that the AssetService handles a FileNotFoundError gracefully."""
    # Create a config that points to a file that doesn't exist
    config_data = {
        "spritesheets": {
            "bad_sheet": {
                "file": "non_existent_sheet.bmp",
                "sprite_width": 16,
                "sprite_height": 16,
                "colorkey": [0, 0, 0],
            }
        }
    }
    with open(assets_config_file, "w") as f:
        json.dump(config_data, f)

    AssetService(assets_config_path=assets_config_file)
    captured = capsys.readouterr()
    assert "Warning: Could not load spritesheets. File error:" in captured.out


def test_asset_service_handles_pygame_error(
    assets_config_file: Path, temp_asset_dir: str, capsys
):
    """Tests that the AssetService handles a pygame.error gracefully."""
    # Create dummy asset files
    (Path(temp_asset_dir) / "icons").mkdir()
    (Path(temp_asset_dir) / "icons" / "dummy.bmp").touch()
    (Path(temp_asset_dir) / "sheet.bmp").touch()

    config_data = {
        "images": {"dummy_image": {"dir": "icons"}},
        "spritesheets": {
            "dummy_sheet": {
                "file": "sheet.bmp",
                "sprite_width": 16,
                "sprite_height": 16,
                "colorkey": [255, 0, 255],
            }
        },
    }
    with open(assets_config_file, "w") as f:
        json.dump(config_data, f)

    # Patch pygame.image.load to simulate a failure and patch GFX.asset_folder
    # so loaders look at our temp directory created above.
    with (
        patch(
            "decker_pygame.presentation.asset_loader.pygame.image.load",
            side_effect=pygame.error("Test error"),
        ),
        patch(
            "decker_pygame.presentation.asset_service.GFX.asset_folder",
            Path(temp_asset_dir),
        ),
    ):
        AssetService(assets_config_path=assets_config_file)

    captured = capsys.readouterr()
    assert "Warning: Could not load spritesheets. Pygame error:" in captured.out
    assert "Warning: Could not load images. Pygame error:" in captured.out
