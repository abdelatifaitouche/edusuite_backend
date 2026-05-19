from pydantic import BaseModel
from datetime import date, time
from uuid import UUID
from src.features.training.enums.session import SessionOccurenceState


class OccurrenceCompact(BaseModel):
    session_number: int
    session_id: UUID
    formateur_name: str
    formation_name: str
    planned_date: date
    start_at: time
    end_date: time
    status: SessionOccurenceState
    id: UUID
    model_config = {"from_attributes": True}


class ReadOccurrence(BaseModel):
    session_id: UUID
    planned_date: date
    start_at: time
    end_at: time
    status: SessionOccurenceState
    notes: str

    id: UUID

    model_config = {"from_attributes": True}
