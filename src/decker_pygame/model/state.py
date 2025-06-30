from decker_pygame.model.character import Character
from decker_pygame.model.contract import Contract
from pydantic import BaseModel, Field


class GameState(BaseModel):
    """Represents the entire state of the game at any given moment."""

    player_character: Character
    active_contracts: list[Contract] = Field(default_factory=list)
    current_location_id: int
    game_time: int = 0  # e.g., in-game seconds elapsed
    # You can add other global state variables here, like alert levels, etc.
