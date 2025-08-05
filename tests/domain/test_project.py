"""This module contains tests for the domain objects related to the R&D system."""

from decker_pygame.domain.project import ActiveProject, ProjectType


def test_active_project_serialization():
    """Tests that ActiveProject can be serialized to and from a dictionary."""
    project = ActiveProject(
        project_type=ProjectType.SOFTWARE,
        item_class="Sentry ICE",
        target_rating=1,
        time_required=100,
        time_spent=25,
    )

    data = project.to_dict()

    assert data == {
        "project_type": "software",
        "item_class": "Sentry ICE",
        "target_rating": 1,
        "time_required": 100,
        "time_spent": 25,
    }

    reconstituted_project = ActiveProject.from_dict(data)
    assert reconstituted_project is not None
    assert reconstituted_project == project


def test_active_project_from_dict_with_none():
    """Tests that from_dict returns None when given None."""
    assert ActiveProject.from_dict(None) is None
