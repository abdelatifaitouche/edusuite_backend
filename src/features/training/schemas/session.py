from pydantic import BaseModel
from uuid import UUID
from datetime import date, time

from src.features.training.enums.session import SessionState, PlanningType
from src.features.training.schemas.session_reccurrence import CreateRecurrenceRule


class CreateSession(BaseModel):
    formation_id: UUID
    formateur_id: UUID
    salle_id: UUID
    type_planning: PlanningType
    date_debut: date  # first occurrence
    date_fin: date  # last occurrence

    r_rule: CreateRecurrenceRule


class ReadSession(BaseModel):
    formation_id: UUID
    formateur_id: UUID
    salle_id: UUID | None
    statut: SessionState
    type_planning: PlanningType
    date_debut: date  # first occurrence
    date_fin: date  # last occurrence

    r_rule_id: UUID

    model_config = {"from_attributes": True}
