import json
import os
from typing import Any

from decker_pygame.domain.contract import Contract
from decker_pygame.domain.contract_repository_interface import (
    ContractRepositoryInterface,
)
from decker_pygame.domain.ids import ContractId


class JsonFileContractRepository(ContractRepositoryInterface):
    """A repository that stores contract data in JSON files."""

    def __init__(self, base_path: str):
        self.base_path = base_path
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def _get_path(self, contract_id: ContractId) -> str:
        return os.path.join(self.base_path, f"{contract_id}.json")

    def get(self, contract_id: ContractId) -> Contract | None:
        filepath = self._get_path(contract_id)
        if not os.path.exists(filepath):
            return None
        with open(filepath) as f:
            data = json.load(f)
        return Contract.from_dict(data)

    def save(self, contract: Contract) -> None:
        filepath = self._get_path(ContractId(contract.id))
        with open(filepath, "w") as f:
            json.dump(contract.to_dict(), f, indent=4)

    def get_all(self) -> list[Contract]:
        contracts: list[Contract] = []
        if not os.path.exists(self.base_path):
            return contracts

        for filename in os.listdir(self.base_path):
            if filename.endswith(".json"):
                filepath = os.path.join(self.base_path, filename)
                try:
                    with open(filepath) as f:
                        data: dict[str, Any] = json.load(f)
                        contracts.append(Contract.from_dict(data))
                except (json.JSONDecodeError, KeyError):
                    # Skip corrupted or invalid files
                    continue
        return contracts
