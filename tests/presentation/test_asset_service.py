"""This module contains tests for the AssetService."""

import json
from pathlib import Path
from unittest.mock import patch

import pygame
import pytest

from decker_pygame.presentation.asset_service import AssetService


@pytest.fixture(autouse=True)
def pygame_init_fixture():
    """Fixture to initialize pygame for each test."""
    pygame.init()
    yield
    pygame.quit()


@pytest.fixture
def mock_assets_json(tmp_path: Path) -> Path:
    """Creates a mock assets.json file in a temporary directory."""
    assets_dir = tmp_path / "data"
    assets_dir.mkdir()
    config_path = assets_dir / "assets.json"

    config_data = {
        "spritesheets": {
            "test_sheet": {
                "file": "test_sprites.bmp",
                "sprite_width": 16,
                "sprite_height": 16,
                "colorkey": [255, 0, 255],
            }
        }
    }

    with open(config_path, "w") as f:
        json.dump(config_data, f)

    return config_path


def test_asset_service_initialization_and_loading(mock_assets_json: Path):
    """Tests that the AssetService correctly loads data from the config file."""
    mock_surface = pygame.Surface((16, 16))

    with patch(
        "decker_pygame.presentation.asset_service.load_spritesheet"
    ) as mock_load:
        mock_load.return_value = ([mock_surface], (16, 16))

        service = AssetService(assets_config_path=mock_assets_json)

        mock_load.assert_called_once()
        retrieved_sheet = service.get_spritesheet("test_sheet")
        assert retrieved_sheet == [mock_surface]


def test_get_spritesheet_not_found(mock_assets_json: Path):
    """Tests that get_spritesheet returns an empty list for a non-existent sheet."""
    # The mock needs a valid return value to be unpacked in the service's __init__
    with patch(
        "decker_pygame.presentation.asset_service.load_spritesheet",
        return_value=([pygame.Surface((16, 16))], (16, 16)),
    ):
        service = AssetService(assets_config_path=mock_assets_json)

        retrieved_sheet = service.get_spritesheet("non_existent_sheet")
        assert retrieved_sheet == []
