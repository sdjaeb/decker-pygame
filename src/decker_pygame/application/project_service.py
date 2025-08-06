"""This module defines the application service for the R&D system."""

import random
from typing import Optional
from uuid import uuid4

from decker_pygame.application.dtos import (
    NewProjectViewDTO,
    ProjectDataViewDTO,
    SourceCodeDTO,
)
from decker_pygame.application.event_dispatcher import EventDispatcher
from decker_pygame.domain.crafting import RequiredResource, Schematic
from decker_pygame.domain.ids import CharacterId, SchematicId
from decker_pygame.domain.project import ActiveProject, ProjectType
from decker_pygame.ports.repository_interfaces import CharacterRepositoryInterface
from decker_pygame.ports.service_interfaces import ProjectServiceInterface


class ProjectError(Exception):
    """Base exception for R&D project-related errors."""

    pass


class ProjectService(ProjectServiceInterface):
    """Application service for managing R&D projects."""

    def __init__(
        self,
        character_repo: CharacterRepositoryInterface,
        event_dispatcher: EventDispatcher,
    ):
        self._character_repo = character_repo
        self._event_dispatcher = event_dispatcher

    def get_project_data_view_data(
        self, character_id: CharacterId
    ) -> Optional[ProjectDataViewDTO]:
        """Retrieves a comprehensive DTO for the project management view."""
        character = self._character_repo.get(character_id)
        if not character:
            return None

        # Project Info
        project_type_str = "None"
        project_time_left_str = ""
        if character.active_project:
            proj = character.active_project
            project_type_str = f"{proj.item_class} - {proj.target_rating}"
            # This is a simplification; original game logic is more complex
            project_time_left_str = f"{proj.time_required - proj.time_spent} TU"

        # Chip Burning Info (placeholder)
        chip_type_str = "None"
        chip_time_left_str = ""

        # Source Code Info
        source_codes = []
        for schematic in character.schematics:
            # This is a simplification. We'd normally check installed software/chips.
            current_rating = "-"
            source_codes.append(
                SourceCodeDTO(
                    id=str(schematic.id),
                    type=schematic.type.value,
                    name=schematic.produces_item_name,
                    rating=schematic.rating,
                    current_rating=current_rating,
                )
            )

        return ProjectDataViewDTO(
            date="Jan 1, 2072",  # Placeholder
            project_type=project_type_str,
            project_time_left=project_time_left_str,
            chip_type=chip_type_str,
            chip_time_left=chip_time_left_str,
            source_codes=source_codes,
            can_start_new_project=character.active_project is None,
            can_work_on_project=character.active_project is not None,
        )

    def get_new_project_data(
        self, character_id: CharacterId
    ) -> Optional[NewProjectViewDTO]:
        """Retrieves data needed to start a new project for the UI."""
        character = self._character_repo.get(character_id)
        if not character:
            return None

        # In a real implementation, this would come from a master item list
        # or some other configuration source.
        available_software = ["Sentry ICE", "Hammer", "IcePick"]
        available_chips = ["Cortex Bomb", "Encephalon"]

        return NewProjectViewDTO(
            programming_skill=character.skills.get("Programming", 0),
            chip_design_skill=character.skills.get("Chip Design", 0),
            available_software=available_software,
            available_chips=available_chips,
        )

    def start_new_project(
        self, character_id: CharacterId, item_type: str, item_class: str, rating: int
    ) -> None:
        """Starts a new research project for the character."""
        character = self._character_repo.get(character_id)
        if not character:
            raise ProjectError(f"Character with ID {character_id} not found.")

        if character.active_project:
            raise ProjectError("Character already has an active project.")

        # Determine relevant skill
        skill_map = {
            ProjectType.SOFTWARE.value: "Programming",
            ProjectType.CHIP.value: "Chip Design",
        }
        relevant_skill = skill_map.get(item_type)
        if not relevant_skill:
            raise ProjectError(f"Invalid item type for project: {item_type}")

        skill_level = character.skills.get(relevant_skill, 0)

        # Find highest existing rating for this item class to reduce research time
        highest_existing_rating = 0
        for schematic in character.schematics:
            if item_class == schematic.produces_item_name:
                highest_existing_rating = max(highest_existing_rating, schematic.rating)

        # Calculate time required based on original game's formula
        time_required = rating * rating * 100
        time_required -= highest_existing_rating * highest_existing_rating * 25
        time_required -= skill_level * skill_level * 10
        time_required = max(time_required, 10)

        project = ActiveProject(
            project_type=ProjectType(item_type),
            item_class=item_class,
            target_rating=rating,
            time_required=time_required,
            time_spent=0,
        )

        character.start_new_project(project)
        self._character_repo.save(character)

    def work_on_project(self, character_id: CharacterId, time_to_add: int) -> None:
        """Adds time to the character's active project."""
        character = self._character_repo.get(character_id)
        if not character:
            raise ProjectError(f"Character with ID {character_id} not found.")

        # The domain object also checks this, but it's good practice for the
        # service to validate preconditions before attempting the operation.
        if not character.active_project:
            raise ProjectError("Character has no active project to work on.")

        character.work_on_project(time_to_add)
        self._character_repo.save(character)

    def complete_project(self, character_id: CharacterId) -> None:
        """Checks if the project is finished.

        If so, performs a skill check and awards a schematic on success.
        """
        character = self._character_repo.get(character_id)
        if not character:
            raise ProjectError(f"Character with ID {character_id} not found.")

        project = character.active_project
        if not project:
            raise ProjectError("Character has no active project to complete.")

        if project.time_spent < project.time_required:
            raise ProjectError("Project is not yet complete. More time required.")

        # Determine relevant skill
        skill_map = {"software": "Programming", "chip": "Chip Design"}
        relevant_skill = skill_map.get(project.project_type.value)
        if not relevant_skill:
            # This should not happen if start_new_project is used correctly
            raise ProjectError(
                f"Invalid item type in active project: {project.project_type.value}"
            )

        skill_level = character.skills.get(relevant_skill, 0)

        # Perform skill check (e.g., roll a d10, must be <= skill level)
        if random.randint(1, 10) <= skill_level:
            # Success! Create and award the schematic.
            new_schematic = Schematic(
                id=SchematicId(uuid4()),
                name=f"{project.item_class} v{project.target_rating} Schematic",
                produces_item_name=f"{project.item_class} v{project.target_rating}",
                produces_item_size=project.target_rating * 20,  # Placeholder logic
                rating=project.target_rating,
                cost=[
                    RequiredResource("credits", project.target_rating * 100)
                ],  # Placeholder logic
                type=project.project_type,
            )
            character.schematics.append(new_schematic)

        # Project is consumed regardless of success
        character.complete_project()
        self._character_repo.save(character)

    def build_from_schematic(
        self, character_id: CharacterId, schematic_id: str
    ) -> None:
        """Builds an item from a known schematic by its ID."""
        character = self._character_repo.get(character_id)
        if not character:
            raise ProjectError(f"Character with ID {character_id} not found.")

        try:
            schematic_to_use = next(
                s for s in character.schematics if str(s.id) == schematic_id
            )
        except StopIteration:
            raise ProjectError(
                f"Schematic with ID '{schematic_id}' not found for character."
            ) from None

        try:
            character.craft(schematic_to_use)
        except ValueError as e:
            # Translate domain error into application-specific error
            raise ProjectError(str(e)) from e

        self._character_repo.save(character)
        self._event_dispatcher.dispatch(character.events)
        character.clear_events()

    def trash_schematic(self, character_id: CharacterId, schematic_id: str) -> None:
        """Deletes a known schematic."""
        character = self._character_repo.get(character_id)
        if not character:
            raise ProjectError(f"Character with ID {character_id} not found.")

        initial_count = len(character.schematics)
        character.schematics = [
            s for s in character.schematics if str(s.id) != schematic_id
        ]

        if len(character.schematics) == initial_count:
            raise ProjectError(
                f"Schematic with ID '{schematic_id}' not found for character."
            )

        self._character_repo.save(character)
