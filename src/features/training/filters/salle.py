from pydantic import BaseModel
from src.features.training.enums.salle import SalleState


class SalleFilters(BaseModel):
    status: SalleState | None = None
    size: int | None = None
