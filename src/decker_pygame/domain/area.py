from decker_pygame.domain.aggregate import AggregateRoot
from decker_pygame.domain.contract import Contract
from decker_pygame.domain.ids import AggregateId, AreaId, ContractId


class Area(AggregateRoot):
    """Represents a location or region in the game world."""

    def __init__(
        self,
        id: AreaId,
        name: str,
        description: str,
        security_level: int,
    ) -> None:
        super().__init__(id=AggregateId(id))
        self.name = name
        self.description = description
        self.security_level = security_level
        self.contract_ids: list[ContractId] = []

    def add_contract(self, contract: Contract) -> None:
        """Adds a new contract to the area, enforcing business rules."""
        # This is where you would enforce invariants, for example:
        # if self.security_level < 5 and contract.reward_credits > 10000:
        #     raise ValueError("High-value contracts cannot be in low-security areas.")
        self.contract_ids.append(ContractId(contract.id))
