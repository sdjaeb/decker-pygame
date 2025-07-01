"""
Global settings and constants for the game.

This file centralizes configuration values that were likely in Global.h/cpp,
making them easy to adjust.
"""

from pathlib import Path

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
    asset_folder: Path = Path(__file__).resolve().parent.parent.parent / "assets"
    program_icon_sheet: str = "programs.bmp"
    program_icon_source_size: int = 16
    active_bar_image_size: int = 32
    active_bar_max_slots: int = 8


GFX = GfxSettings()


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

# --- Gameplay Constants ---
MAX_ALERT_LEVEL = 100.0
