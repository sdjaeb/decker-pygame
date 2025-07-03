from decker_pygame.domain.entity import Entity
from decker_pygame.domain.ids import AreaId, ContractId


class Contract(Entity):
    """Represents a job or mission a character can undertake."""

    def __init__(
        self,
        id: ContractId,
        title: str,
        client: str,
        target_area_id: AreaId,
        description: str,
        reward_credits: int,
    ) -> None:
        super().__init__(id=id)
        self.title = title
        self.client = client
        self.target_area_id = target_area_id
        self.description = description
        self.reward_credits = reward_credits
