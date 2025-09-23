"""This module defines the AssetService for loading and managing game assets."""

import json
from pathlib import Path
from typing import Any

import pygame

from decker_pygame.presentation.asset_loader import load_images, load_spritesheet
from decker_pygame.settings import GFX


class AssetService:
    """A service to load and manage game assets from a configuration file."""

    def __init__(self, assets_config_path: Path):
        self._config_path = assets_config_path
        # Maps of loaded assets. Images may be None when loading fails or the
        # directory is empty; reflect that in the type to keep static checks
        # happy.
        self._spritesheets: dict[str, list[pygame.Surface]] = {}
        self._images: dict[str, pygame.Surface | None] = {}
        self._load_assets()

    def _load_assets(self) -> None:
        """Loads all assets defined in the configuration file."""
        with open(self._config_path) as f:
            config = json.load(f)

        self._load_spritesheets(config.get("spritesheets", {}))
        self._load_images(config.get("images", {}))

    def _load_spritesheets(self, spritesheet_configs: dict[str, Any]) -> None:
        """Loads all spritesheets from the provided configuration."""
        try:
            for name, sheet_data in spritesheet_configs.items():
                surfaces, _ = load_spritesheet(
                    filename=sheet_data["file"],
                    sprite_width=sheet_data["sprite_width"],
                    sprite_height=sheet_data["sprite_height"],
                    colorkey=tuple(sheet_data["colorkey"]),
                    base_path=GFX.asset_folder,
                )
                self._spritesheets[name] = surfaces
        except FileNotFoundError as e:
            print(f"Warning: Could not load spritesheets. File error: {e}")
        except pygame.error as e:
            print(f"Warning: Could not load spritesheets. Pygame error: {e}")

    def _load_images(self, image_configs: dict[str, Any]) -> None:
        """Loads all single images from the provided configuration."""
        try:
            for name, image_data in image_configs.items():
                # Assuming image_data["dir"] is a subdirectory like "programs"
                # and image_data["size"] is an optional [width, height] list.
                images = load_images(
                    base_path=GFX.asset_folder,
                    subdirectory=image_data["dir"],
                    size=tuple(image_data["size"]) if "size" in image_data else None,
                )
                # If no images were loaded, leave as None; otherwise use the
                # first image found. This avoids IndexError during tests where
                # asset dirs may be empty or missing.
                self._images[name] = images[0] if images else None
        except pygame.error as e:
            print(f"Warning: Could not load images. Pygame error: {e}")

    def get_spritesheet(self, name: str) -> list[pygame.Surface]:
        """Retrieves a loaded spritesheet by name."""
        return self._spritesheets.get(name, [])

    def get_image(self, name: str) -> pygame.Surface | None:
        """Retrieves a loaded image by name."""
        return self._images.get(name)
