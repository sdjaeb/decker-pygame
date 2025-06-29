from dataclasses import dataclass
from pathlib import Path

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
    """A container for graphics-related settings."""

    asset_folder: Path = ASSETS_DIR
    active_bar_image_size: int = 48
    active_bar_max_slots: int = 8


# Global instance of the graphics configuration
GFX = GraphicsConfig()
