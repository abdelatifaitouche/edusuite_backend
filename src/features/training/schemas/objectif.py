from pydantic import BaseModel
from uuid import UUID


class ObjectifRead(BaseModel):
    id: UUID
    formation_id: UUID
    titre: str
    order: int

    model_config = {"from_attributes": True}


class ObjectifCreate(BaseModel):
    titre: str
    order: int


class ObjectifUpdate(BaseModel):
    titre: str | None = None
    order: int | None = None
