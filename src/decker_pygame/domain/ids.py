import uuid
from typing import NewType

AggregateId = NewType("AggregateId", uuid.UUID)
AreaId = NewType("AreaId", uuid.UUID)
CharacterId = NewType("CharacterId", uuid.UUID)
ContractId = NewType("ContractId", uuid.UUID)
PlayerId = NewType("PlayerId", uuid.UUID)
