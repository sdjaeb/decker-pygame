from pathlib import Path
from dataclasses import dataclass

# --- Game Settings ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Decker-Pygame"

# --- Paths ---
# Use Path for cross-platform compatibility
ASSETS_DIR = Path(__file__).resolve().parent.parent.parent / "assets"
DEFAULT_GRAPHICS_DIR = ASSETS_DIR / "DefaultGraphics"
RES_DIR = ASSETS_DIR / "res"

# --- Colors ---
BLACK = (0, 0, 0)
# The original C++ code used GetSysColor(COLOR_3DFACE), which is a light gray.
# RGB(212, 208, 200) is a common equivalent.
UI_FACE = (212, 208, 200)
# --- Asset Configurations ---

@dataclass(frozen=True)
class GraphicsConfig:
    """A dataclass to hold paths to all graphics assets."""
    # Path to the program icons spritesheet, identified from asset file list.
    program_icon_sheet: Path = RES_DIR / "software_il.bmp"

    # ActiveBar component settings
    active_bar_image_size: int = 16
    active_bar_max_slots: int = 6


# Global instance of the graphics configuration
GFX = GraphicsConfig()