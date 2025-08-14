"""This module contains tests for the DSFile domain model."""

import uuid

from decker_pygame.domain.ds_file import DSFile, DSFileType
from decker_pygame.domain.ids import DSFileId


def test_ds_file_initialization():
    """Tests that a DSFile can be initialized correctly."""
    file_id = DSFileId(uuid.uuid4())
    ds_file = DSFile(
        id=file_id,
        name="accounts.dat",
        file_type=DSFileType.DATA,
        size=10,
        content="[...]",
    )

    assert ds_file.id == file_id
    assert ds_file.name == "accounts.dat"
    assert ds_file.file_type == DSFileType.DATA
    assert ds_file.size == 10
    assert ds_file.content == "[...]"


def test_ds_file_serialization():
    """Tests that a DSFile can be serialized to and from a dictionary."""
    file_id = DSFileId(uuid.uuid4())
    original_file = DSFile(
        id=file_id,
        name="accounts.dat",
        file_type=DSFileType.DATA,
        size=10,
        content="[...]",
    )

    data = original_file.to_dict()

    expected_data = {
        "id": str(file_id),
        "name": "accounts.dat",
        "file_type": "data",
        "size": 10,
        "content": "[...]",
    }
    assert data == expected_data

    reconstituted_file = DSFile.from_dict(data)
    assert reconstituted_file.id == original_file.id
    assert reconstituted_file.name == original_file.name
    assert reconstituted_file.file_type == original_file.file_type
    assert reconstituted_file.size == original_file.size
    assert reconstituted_file.content == original_file.content
