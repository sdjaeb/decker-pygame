from pathlib import Path

# --- Game Settings ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Decker-Pygame"

# --- Paths ---
# Use Path for cross-platform compatibility
ASSETS_DIR = Path(__file__).parent.parent / "assets"
RES_DIR = ASSETS_DIR / "res"

# --- Colors ---
BLACK = (0, 0, 0)
# The original C++ code used GetSysColor(COLOR_3DFACE), which is a light gray.
# RGB(212, 208, 200) is a common equivalent.
UI_FACE = (212, 208, 200)

# --- Component-specific constants ---
# ActiveBar
MAX_ACTIVE = 6
ACTIVE_IMAGE_SIZE = 16
PROGRAM_ICON_SHEET = RES_DIR / "programs.bmp"