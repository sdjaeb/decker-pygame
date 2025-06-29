from dataclasses import dataclass
from pathlib import Path

# --- Asset Subdirectory Names ---
PROGRAM_BMPS_DIR_NAME = "program_bmps"
SOUNDS_DIR_NAME = "sounds"

# --- Asset Configurations ---
# (Classes are alphabetized below)

# --- Colors ---
BLACK = (0, 0, 0)
DK_GREEN = (0, 128, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
TRANSPARENT_COLOR = BLACK
UI_FACE = (212, 208, 200)
YELLOW = (255, 255, 0)

# --- Game Settings ---
FPS = 60
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
TITLE = "Decker-Pygame"

# --- Paths ---
ASSETS_DIR = Path(__file__).resolve().parent.parent.parent / "assets"
DEFAULT_GRAPHICS_DIR = ASSETS_DIR / "DefaultGraphics"
RES_DIR = ASSETS_DIR / "res"


@dataclass(frozen=True)
class AlarmConfig:
    """A container for alarm-bar-related settings."""

    width: int = 84
    height: int = 8
    colors: tuple[tuple[int, int, int], ...] = (DK_GREEN, YELLOW, RED)
    crash_color: tuple[int, int, int] = PURPLE


# Global instance of the alarm configuration
ALARM = AlarmConfig()


@dataclass(frozen=True)
class GraphicsConfig:
    """A container for graphics-related settings."""

    asset_folder: Path = ASSETS_DIR
    program_icon_source_size: int = 16
    active_bar_image_size: int = 48
    active_bar_max_slots: int = 8
    program_icon_sheet: str = f"{PROGRAM_BMPS_DIR_NAME}/software_il.bmp"


# Global instance of the graphics configuration
GFX = GraphicsConfig()
