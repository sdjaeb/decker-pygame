"""A JSON file-based implementation of the DSFile repository interface."""

import json
import os
from typing import Optional

from decker_pygame.domain.ds_file import DSFile
from decker_pygame.domain.ids import DSFileId
from decker_pygame.ports.repository_interfaces import DSFileRepositoryInterface


class JsonFileDSFileRepository(DSFileRepositoryInterface):
    """A concrete repository that persists DSFile aggregates to a single JSON file.

    This repository loads all DSFiles into memory on initialization.

    Args:
        file_path (str): The path to the JSON file.
    """

    def __init__(self, file_path: str) -> None:
        self._file_path = file_path
        self._ds_files: dict[DSFileId, DSFile] = {}
        self._load()

    def _load(self) -> None:
        """Load all DSFiles from the JSON file into memory."""
        if not os.path.exists(self._file_path):
            return

        try:
            with open(self._file_path) as f:
                data = json.load(f)
            for file_data in data.get("ds_files", []):
                ds_file = DSFile.from_dict(file_data)
                self._ds_files[DSFileId(ds_file.id)] = ds_file
        except (json.JSONDecodeError, KeyError):
            # Handle corrupted or empty file gracefully.
            pass

    def save(self, ds_file: DSFile) -> None:
        """Save a DSFile aggregate. Not yet implemented (read-only repo)."""
        # This repository is intended for read-only game data for now.
        # A full implementation would write back to the file.
        raise NotImplementedError("Saving DSFiles is not supported yet.")

    def get(self, ds_file_id: DSFileId) -> Optional[DSFile]:
        """Retrieve a DSFile aggregate by its ID."""
        return self._ds_files.get(ds_file_id)
