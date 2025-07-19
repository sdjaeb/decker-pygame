"""This module defines the application service for the R&D system."""

import random
from typing import Optional

from decker_pygame.application.dtos import NewProjectViewDTO, ProjectDataViewDTO
from decker_pygame.domain.crafting import RequiredResource, Schematic
from decker_pygame.domain.ids import CharacterId
from decker_pygame.domain.project import ActiveProject
from decker_pygame.ports.repository_interfaces import CharacterRepositoryInterface
from decker_pygame.ports.service_interfaces import ProjectServiceInterface


class ProjectError(Exception):
    """Base exception for R&D project-related errors."""

    pass


class ProjectService(ProjectServiceInterface):
    """Application service for managing R&D projects."""

    def __init__(self, character_repo: CharacterRepositoryInterface):
        self._character_repo = character_repo

    def get_project_data(
        self, character_id: CharacterId
    ) -> Optional[ProjectDataViewDTO]:
        """Retrieves data about the character's active project for the UI."""
        character = self._character_repo.get(character_id)
        if not character or not character.active_project:
            return None

        project = character.active_project
        return ProjectDataViewDTO(
            item_class=project.item_class,
            target_rating=project.target_rating,
            time_required=project.time_required,
            time_spent=project.time_spent,
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
        skill_map = {"software": "Programming", "chip": "Chip Design"}
        relevant_skill = skill_map.get(item_type)
        if not relevant_skill:
            raise ProjectError(f"Invalid item type for project: {item_type}")

        skill_level = character.skills.get(relevant_skill, 0)

        # Find highest existing rating for this item class to reduce research time
        highest_existing_rating = 0
        for schematic in character.schematics:
            # A simple check for now; could be more robust
            if item_class in schematic.produces_item_name:
                highest_existing_rating = max(highest_existing_rating, schematic.rating)

        # Calculate time required based on original game's formula
        time_required = rating * rating * 100
        time_required -= highest_existing_rating * highest_existing_rating * 25
        time_required -= skill_level * skill_level * 10
        time_required = max(time_required, 10)

        project = ActiveProject(
            item_type=item_type,
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
        relevant_skill = skill_map.get(project.item_type)
        if not relevant_skill:
            # This should not happen if start_new_project is used correctly
            raise ProjectError(
                f"Invalid item type in active project: {project.item_type}"
            )

        skill_level = character.skills.get(relevant_skill, 0)

        # Perform skill check (e.g., roll a d10, must be <= skill level)
        if random.randint(1, 10) <= skill_level:
            # Success! Create and award the schematic.
            new_schematic = Schematic(
                name=f"{project.item_class} v{project.target_rating} Schematic",
                produces_item_name=f"{project.item_class} v{project.target_rating}",
                produces_item_size=project.target_rating * 20,  # Placeholder logic
                rating=project.target_rating,
                cost=[
                    RequiredResource("credits", project.target_rating * 100)
                ],  # Placeholder logic
            )
            character.schematics.append(new_schematic)

        # Project is consumed regardless of success
        character.complete_project()
        self._character_repo.save(character)
