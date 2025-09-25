import json
from pathlib import Path

import pygame

from decker_pygame.presentation.asset_service import AssetService


def make_temp_config(tmp_path: Path, content: dict) -> Path:
    p = tmp_path / "assets_test.json"
    p.write_text(json.dumps(content))
    return p


def test_dir_entry_with_no_images_returns_none(tmp_path: Path, monkeypatch):
    # Arrange: load_images returns an empty list -> service should set None
    cfg = {"images": {"empty_dir": {"dir": "no_such_dir"}}}
    cfg_path = make_temp_config(tmp_path, cfg)

    monkeypatch.setattr(
        "decker_pygame.presentation.asset_loader.load_images",
        lambda base_path, subdirectory, size=None: [],
    )

    # Act
    svc = AssetService(cfg_path)

    # Assert
    assert svc.get_image("empty_dir") is None


def test_file_entry_not_found_sets_none(tmp_path: Path, monkeypatch):
    # Arrange: point to a file that doesn't exist and ensure FileNotFoundError
    cfg = {"images": {"missing_file": {"file": "nope.bmp"}}}
    cfg_path = make_temp_config(tmp_path, cfg)

    def fake_load(path):
        raise FileNotFoundError(path)

    monkeypatch.setattr("pygame.image.load", fake_load)

    svc = AssetService(cfg_path)
    assert svc.get_image("missing_file") is None


def test_file_entry_convert_alpha_falls_back(monkeypatch, tmp_path: Path):
    # Arrange: simulate pygame.image.load returning an object whose
    # convert_alpha raises pygame.error; ensure code falls back to loaded.
    cfg = {"images": {"img": {"file": "some.bmp"}}}
    cfg_path = make_temp_config(tmp_path, cfg)

    class FakeSurface:
        def convert_alpha(self):
            raise pygame.error("no alpha")

    def fake_load(path):
        return FakeSurface()

    monkeypatch.setattr("pygame.image.load", fake_load)

    svc = AssetService(cfg_path)
    surf = svc.get_image("img")
    assert surf is not None
