"""This module contains tests for the DSFileService."""

import uuid

import pytest

from decker_pygame.application.ds_file_service import DSFileService
from decker_pygame.domain.ds_file import DSFile, DSFileType
from decker_pygame.domain.ids import DSFileId
from decker_pygame.infrastructure.in_memory_ds_file_repository import (
    InMemoryDSFileRepository,
)


@pytest.fixture
def ds_file_repo():
    """Fixture for an in-memory DSFile repository."""
    return InMemoryDSFileRepository()


@pytest.fixture
def ds_file_service(ds_file_repo):
    """Fixture for the DSFileService."""
    return DSFileService(ds_file_repo=ds_file_repo)


def test_get_ds_file_data_found(ds_file_service, ds_file_repo):
    """Tests that getting DSFile data returns the correct DTO when found."""
    file_id = DSFileId(uuid.uuid4())
    ds_file = DSFile(
        id=file_id,
        name="test.dat",
        file_type=DSFileType.DATA,
        size=123,
        content="test content",
    )
    ds_file_repo.save(ds_file)

    dto = ds_file_service.get_ds_file_data(file_id)

    assert dto is not None
    assert dto.id == file_id
    assert dto.name == "test.dat"
    assert dto.file_type == "data"
    assert dto.size == 123


def test_get_ds_file_data_not_found(ds_file_service):
    """Tests that getting DSFile data returns None when not found."""
    non_existent_id = DSFileId(uuid.uuid4())

    dto = ds_file_service.get_ds_file_data(non_existent_id)

    assert dto is None
