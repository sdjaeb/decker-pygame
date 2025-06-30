from typing import Annotated

from pydantic import BaseModel, Field


class Contract(BaseModel):
    """Represents a job or mission for the player."""

    id: int
    title: str
    description: str
    client: str
    target_area_id: int
    objectives: list[str] = Field(default_factory=list)
    # Ensure reward credits are also non-negative
    reward_credits: Annotated[int, Field(ge=0)] = 0
    is_completed: bool = False
