# Run audit: initial game launch (2025-09-23)

Environment
- Branch: `audit/run-audit` (created from current working tree)
- Platform: macOS
- Python: 3.13.3 (project `.venv`)
- Pygame: pygame-ce 2.5.5

What I ran
1. Activated the project's venv: `source .venv/bin/activate`.
2. Launched the game via the console script: `decker`.

Observed output / failure
```
pygame-ce 2.5.5 (SDL 2.32.6, Python 3.13.3)
--- Decker Game Initializing ---
Traceback (most recent call last):
  File "/Users/sdjaeb/dev/decker/decker-pygame/.venv/bin/decker", line 10, in <module>
    sys.exit(main())
             ~~~~^^
  File "/Users/sdjaeb/dev/decker/decker-pygame/src/decker_pygame/presentation/main.py", line 91, in main
    asset_service = AssetService(
        assets_config_path=Path(PATHS.base_path) / "assets.json"
    )
  File "/Users/sdjaeb/dev/decker/decker-pygame/src/decker_pygame/presentation/asset_service.py", line 23, in __init__
    self._load_assets()
    ~~~~~~~~~~~~~~~~~^^
  File "/Users/sdjaeb/dev/decker/decker-pygame/src/decker_pygame/presentation/asset_service.py", line 31, in _load_assets
    self._load_images(config.get("images", {}))
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/sdjaeb/dev/decker/decker-pygame/src/decker_pygame/presentation/asset_service.py", line 58, in _load_images
    subdirectory=image_data["dir"],
                 ~~~~~~~~~~^^^^^^^
KeyError: 'dir'
```

Probable cause
- `data/assets.json` currently defines single images using a `file` key, for example:

```json
"images": {
  "matrix_main": { "file": "ui_bmps/matrix_main.bmp" }
}
```

- `AssetService._load_images` (in `presentation/asset_service.py`) expects `image_data` entries to include a `dir` key and treats them as directories to scan via `load_images(...)`.

- In short, there's a format mismatch between `data/assets.json` and the `AssetService` code: `file` vs `dir`.

Immediate reproduction steps
1. From repo root, activate venv: `source .venv/bin/activate`.
2. Run `decker`.
3. Observe the KeyError as captured above.

Minimal next actions (do not change code in this branch unless you want me to)
- Option A (data fix): Update `data/assets.json` to provide `images` entries in the directory-based shape expected by `AssetService` (use `dir` + optionally `size`), or add a separate `single_images` key and update the code later to support it.
- Option B (code fix): Make `AssetService._load_images` accept either a `file` entry (single image) or a `dir` entry (directory of images). This is more flexible and likely the long-term better option.

Notes for follow-up
- I did not change any code; I recorded this as part of the run audit. If you'd like I can try the quick data-only workaround (edit `data/assets.json` to match expectations) to let the game proceed so we can inspect UI/behavior manually.

Recorded at: 2025-09-23 by automated run audit.
