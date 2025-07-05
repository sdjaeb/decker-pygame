# player_service.py

import uuid
from dataclasses import dataclass

from decker_pygame.application.event_dispatcher import EventDispatcher
from decker_pygame.domain.ids import PlayerId
from decker_pygame.domain.player import Player
from decker_pygame.domain.player_repository_interface import PlayerRepositoryInterface


class PlayerCreationPreconditionError(Exception):
    """Custom exception raised when preconditions for creating a player are not met."""

    pass


@dataclass(frozen=True)
class PlayerStatusDTO:
    """Data Transfer Object for player status to be displayed in the UI."""

    current_health: int
    max_health: int


class PlayerService:
    """Application service for player-related operations."""

    def __init__(
        self, player_repo: PlayerRepositoryInterface, event_dispatcher: EventDispatcher
    ) -> None:
        """
        Initialize the PlayerService.

        Args:
            player_repo (PlayerRepositoryInterface): Repository for player aggregates.
            event_dispatcher (EventDispatcher): The dispatcher for domain events.
        """
        self.player_repo = player_repo
        self.event_dispatcher = event_dispatcher

    def create_new_player(self, name: str) -> PlayerId:
        """
        Create a new player, save it, and return the new player's ID.

        Args:
            name (str): Name of the new player.

        Returns:
            PlayerId: The ID of the newly created player.
        """
        # This is the correct place to enforce business rules and preconditions.
        # For example, you would query another service or repository to check
        # if the required "Action X" has been completed.
        # has_completed_action_x = self.some_other_repo.get_action_x_status()
        # if not has_completed_action_x:
        #     raise PlayerCreationPreconditionError("Action X must be completed first.")

        player_id = PlayerId(uuid.uuid4())
        player = Player.create(player_id=player_id, name=name, initial_health=100)

        self.player_repo.save(player)

        # Dispatch events only after a successful save
        self.event_dispatcher.dispatch(player.events)
        player.clear_events()

        return PlayerId(player.id)

    def get_player_status(self, player_id: PlayerId) -> PlayerStatusDTO | None:
        """
        Retrieves the current status of a player for UI display.

        Args:
            player_id: The ID of the player to query.

        Returns:
            A DTO with player status, or None if the player is not found.
        """
        player = self.player_repo.get(player_id)
        if not player:
            return None

        # Assuming max health is 100 for now, as defined in Player.create
        return PlayerStatusDTO(current_health=player.health, max_health=100)
