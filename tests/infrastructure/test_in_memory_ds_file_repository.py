"""This module contains tests for the InMemoryDSFileRepository."""

import uuid

from decker_pygame.domain.ds_file import DSFile, DSFileType
from decker_pygame.domain.ids import DSFileId
from decker_pygame.infrastructure.in_memory_ds_file_repository import (
    InMemoryDSFileRepository,
)


def test_save_and_get_ds_file():
    """Tests that a DSFile can be saved and retrieved."""
    repo = InMemoryDSFileRepository()
    file_id = DSFileId(uuid.uuid4())
    ds_file = DSFile(
        id=file_id,
        name="test.dat",
        file_type=DSFileType.DATA,
        size=123,
        content="test content",
    )

    repo.save(ds_file)

    retrieved_file = repo.get(file_id)

    assert retrieved_file is not None
    assert retrieved_file.id == file_id
    assert retrieved_file.name == "test.dat"
    assert retrieved_file.file_type == DSFileType.DATA
    assert retrieved_file.size == 123


def test_get_non_existent_ds_file():
    """Tests that getting a non-existent DSFile returns None."""
    repo = InMemoryDSFileRepository()
    non_existent_id = DSFileId(uuid.uuid4())

    retrieved_file = repo.get(non_existent_id)

    assert retrieved_file is None
