"""This module defines the AssetService for loading and managing game assets."""

import json
from pathlib import Path
from typing import Any

import pygame

from decker_pygame.presentation.asset_loader import load_spritesheet
from decker_pygame.settings import GFX


class AssetService:
    """A service to load and manage game assets from a configuration file."""

    def __init__(self, assets_config_path: Path):
        self._config_path = assets_config_path
        self._spritesheets: dict[str, list[pygame.Surface]] = {}
        self._load_assets()

    def _load_assets(self) -> None:
        """Loads all assets defined in the configuration file."""
        with open(self._config_path) as f:
            config = json.load(f)

        self._load_spritesheets(config.get("spritesheets", {}))

    def _load_spritesheets(self, spritesheet_configs: dict[str, Any]) -> None:
        """Loads all spritesheets from the provided configuration."""
        for name, sheet_data in spritesheet_configs.items():
            file_path = GFX.asset_folder / sheet_data["file"]

            surfaces, _ = load_spritesheet(
                str(file_path),
                sprite_width=sheet_data["sprite_width"],
                sprite_height=sheet_data["sprite_height"],
                colorkey=tuple(sheet_data["colorkey"]),
            )
            self._spritesheets[name] = surfaces

    def get_spritesheet(self, name: str) -> list[pygame.Surface]:
        """Retrieves a loaded spritesheet by name."""
        return self._spritesheets.get(name, [])
