"""
Global settings and constants for the game.

This file centralizes configuration values that were likely in Global.h/cpp,
making them easy to adjust.
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pygame.color import Color

# --- General ---
TITLE = "Decker"
FPS = 60

# --- Screen Dimensions ---
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

# --- Colors ---
BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)
TRANSPARENT_COLOR = Color(255, 0, 255)  # A common magenta colorkey
UI_FACE = Color(192, 192, 192)  # A standard grey


# --- File Paths & Assets ---
# Using a class as a namespace for graphics settings
class GfxSettings:
    """A namespace for graphics-related settings and asset paths."""

    asset_folder: Path = Path(__file__).resolve().parent.parent.parent / "assets"
    program_icon_sheet: str = "program_bmps/software_il.bmp"
    program_icon_source_size: int = 16
    active_bar_image_size: int = 32
    active_bar_max_slots: int = 8
    ui_button_sheet: str = "ui_bmps/buttons.bmp"
    ui_button_size: int = 11


GFX = GfxSettings()


# --- Fonts ---
class UiFontSettings:
    """A namespace for UI font settings."""

    default_font_name: str | None = None  # Use pygame default
    default_font_size: int = 18
    default_font_color: Color = Color(200, 200, 200)  # Light grey
    dark_font_color: Color = Color(20, 20, 20)  # Near-black for light backgrounds


UI_FONT = UiFontSettings()


# --- UI Component Settings ---
# Using a class as a namespace for alarm settings
class AlarmSettings:
    width: int = 200
    height: int = 20
    colors: list[Color] = [
        Color(0, 255, 0),  # Green
        Color(255, 255, 0),  # Yellow
        Color(255, 165, 0),  # Orange
        Color(255, 0, 0),  # Red
    ]
    crash_color: Color = Color(0, 0, 255)  # Blue


ALARM = AlarmSettings()


class HealthBarSettings:
    """A namespace for health bar settings."""

    # List of (threshold, color) tuples. The first color whose threshold
    # is exceeded by the health percentage will be used.
    colors: list[tuple[int, Color]] = [
        (50, Color(0, 255, 0)),  # Green for health > 50%
        (25, Color(255, 255, 0)),  # Yellow for health > 25%
        (0, Color(255, 0, 0)),  # Red for health <= 25%
    ]


HEALTH = HealthBarSettings()


class MapViewSettings:
    """A namespace for map view settings."""

    node_color: Color = Color(0, 255, 255)  # Cyan
    node_color_targeted: Color = Color(255, 255, 0)  # Yellow
    node_color_accessed: Color = Color(0, 255, 0)  # Green
    line_color: Color = Color(100, 100, 255)  # Light Blue
    background_color: Color = Color(20, 20, 40)  # Dark Blue
    node_radius: int = 8
    line_width: int = 2


MAP_VIEW = MapViewSettings()

# --- Gameplay Constants ---
MAX_ALERT_LEVEL = 100.0


# --- Development Settings ---
class DevSettings(BaseSettings):
    """Settings for development and debugging, loaded from environment variables."""

    enabled: bool = False

    model_config = SettingsConfigDict(env_prefix="DECKER_DEV_")


DEV_SETTINGS = DevSettings()
