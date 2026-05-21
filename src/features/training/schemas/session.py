from pydantic import BaseModel
from uuid import UUID
from datetime import date, time

from src.features.training.enums.session import SessionState, PlanningType
from src.features.training.schemas.session_reccurrence import CreateRecurrenceRule
from src.features.training.schemas.formation import FormationCompact
from src.features.training.schemas.session_occurrences import ReadOccurrence


class CreateSession(BaseModel):
    formation_id: UUID
    formateur_id: UUID
    salle_id: UUID
    type_planning: PlanningType
    date_debut: date  # first occurrence
    date_fin: date  # last occurrence

    r_rule: CreateRecurrenceRule


class SessionDetails(BaseModel):
    formateur_name: str
    formateur_id: UUID
    formation_title: str
    formation_id: UUID
    start_date: date
    end_date: date
    type_planning: PlanningType
    session_number: str
    status: SessionState
    id: UUID
    occurrences: list[ReadOccurrence]

    model_config = {"from_attributes": True}


class ReadSession(BaseModel):
    session_number: str
    formation_id: UUID
    formateur_id: UUID
    salle_id: UUID | None
    status: SessionState
    type_planinng: PlanningType
    start_date: date  # first occurrence
    end_date: date  # last occurrence

    model_config = {"from_attributes": True}
