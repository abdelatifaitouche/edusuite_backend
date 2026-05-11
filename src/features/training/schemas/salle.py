from pydantic import BaseModel
from uuid import UUID
from src.features.training.enums.salle import SalleState


class SalleCreate(BaseModel):
    name: str
    size: int
    status: SalleState = SalleState.DISPONIBLE


class SalleRead(BaseModel):
    id: UUID
    name: str
    size: int
    status: SalleState

    model_config = {"from_attributes": True}


class SalleUpdate(BaseModel):
    name: str | None = None
    size: int | None = None
    status: SalleState | None = None
