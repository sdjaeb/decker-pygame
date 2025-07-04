from decker_pygame.domain.ddd.aggregate import AggregateRoot
from decker_pygame.domain.ids import AggregateId, AreaId, ContractId


class Area(AggregateRoot):
    """Represents a location or region in the game world."""

    def __init__(
        self,
        id: AreaId,
        name: str,
        description: str,
        security_level: int,
        contract_ids: list[ContractId],
    ) -> None:
        """
        Initialize an Area.

        Args:
            id (AreaId): Unique identifier for the area.
            name (str): Name of the area.
            description (str): Description of the area.
            security_level (int): Security level of the area.
            contract_ids (List[ContractId]): Contracts available in the area.
        """
        super().__init__(id=AggregateId(id))
        self.name = name
        self.description = description
        self.security_level = security_level
        self.contract_ids = contract_ids

    def add_contract(self, contract_id: ContractId) -> None:
        """
        Add a contract to the area.

        Args:
            contract_id (ContractId): The contract to add.

        Returns:
            None
        """
        self.contract_ids.append(contract_id)
