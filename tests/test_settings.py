"""
Tests for the global settings and constants.
"""

from decker_pygame.settings import ALARM, GFX, AlarmSettings, GfxSettings


def test_settings_objects_are_correct_type():
    """Ensures the global settings objects are instantiated correctly."""
    assert isinstance(GFX, GfxSettings)
    assert isinstance(ALARM, AlarmSettings)


def test_asset_paths_exist():
    """
    Verifies that the file paths defined in GfxSettings point to real files.
    This test prevents runtime FileNotFoundError exceptions after refactoring.
    """
    # Construct the full path to the asset
    icon_sheet_path = GFX.asset_folder / GFX.program_icon_sheet

    # Assert that the path exists and is a file
    assert icon_sheet_path.exists(), f"Asset not found at: {icon_sheet_path}"
    assert icon_sheet_path.is_file(), f"Asset path is not a file: {icon_sheet_path}"
