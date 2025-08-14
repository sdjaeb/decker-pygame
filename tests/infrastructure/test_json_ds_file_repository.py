"""This module contains tests for the JsonFileDSFileRepository."""

import json
import os
import uuid
from tempfile import TemporaryDirectory

import pytest

from decker_pygame.domain.ds_file import DSFile, DSFileType
from decker_pygame.domain.ids import DSFileId
from decker_pygame.infrastructure.json_ds_file_repository import (
    JsonFileDSFileRepository,
)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def ds_file_path(temp_dir):
    """Return the path to a temporary ds_files.json file."""
    return os.path.join(temp_dir, "ds_files.json")


def test_save_is_not_implemented(ds_file_path):
    """Tests that save raises NotImplementedError."""
    repo = JsonFileDSFileRepository(ds_file_path)
    file_id = DSFileId(uuid.uuid4())
    ds_file = DSFile(
        id=file_id,
        name="test.dat",
        file_type=DSFileType.DATA,
        size=123,
        content="test content",
    )

    with pytest.raises(NotImplementedError):
        repo.save(ds_file)


def test_get_non_existent_ds_file(ds_file_path):
    """Tests that getting a non-existent DSFile returns None."""
    repo = JsonFileDSFileRepository(ds_file_path)
    non_existent_id = DSFileId(uuid.uuid4())

    retrieved_file = repo.get(non_existent_id)

    assert retrieved_file is None


def test_load_from_existing_file(ds_file_path):
    """Tests that the repository correctly loads data from a pre-existing file."""
    file_id = DSFileId(uuid.uuid4())
    file_data = {
        "ds_files": [
            {
                "id": str(file_id),
                "name": "pre_existing.dat",
                "file_type": "system",
                "size": 1024,
                "content": "system file",
            }
        ]
    }
    with open(ds_file_path, "w") as f:
        json.dump(file_data, f)

    repo = JsonFileDSFileRepository(ds_file_path)
    retrieved_file = repo.get(file_id)

    assert retrieved_file is not None
    assert retrieved_file.name == "pre_existing.dat"
    assert retrieved_file.file_type == DSFileType.SYSTEM


def test_repository_handles_corrupted_json(ds_file_path):
    """Tests that the repository handles a malformed JSON file gracefully."""
    with open(ds_file_path, "w") as f:
        f.write("this is not json")

    repo = JsonFileDSFileRepository(ds_file_path)
    assert repo.get(DSFileId(uuid.uuid4())) is None
