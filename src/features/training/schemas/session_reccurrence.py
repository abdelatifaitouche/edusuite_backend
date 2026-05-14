from pydantic import BaseModel
from uuid import UUID
from datetime import time


class CreateRecurrenceRule(BaseModel):
    session_id: UUID | None = None
    jours_semaine: list[int]  # [0,2] = lundi + mercredi
    heure_debut: time
    heure_fin: time
    intervalle_semaines: int = 1


class ReadRecurrenceRule(BaseModel):
    id: UUID
    session_id: UUID

    jours_semaine: list[int]  # [0,2] = lundi + mercredi
    heure_debut: time
    heure_fin: time
    intervalle_semaines: int = 1
