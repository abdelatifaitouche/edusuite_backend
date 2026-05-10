from pydantic import BaseModel
from uuid import UUID


class ModuleCreate(BaseModel):
    formation_id: UUID | None = None
    titre: str
    order: int
    durée_heure: int
    contenu: str


class ModuleRead(BaseModel):
    id: UUID
    titre: str
    order: int
    durée_heure: int
    contenu: str
    formation_id: UUID | None = None

    model_config = {"from_attributes": True}


class ModuleUpdate(BaseModel):
    titre: str | None = None
