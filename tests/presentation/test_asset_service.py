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
    # Create dummy asset files
    dummy_image_path = Path(temp_asset_dir) / "dummy.bmp"
    pygame.image.save(pygame.Surface((10, 10)), str(dummy_image_path))

    dummy_sheet_path = Path(temp_asset_dir) / "sheet.bmp"
    pygame.image.save(pygame.Surface((32, 16)), str(dummy_sheet_path))

    # Create the assets.json content
    config_data = {
        "images": {"dummy_image": {"file": "dummy.bmp"}},
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
