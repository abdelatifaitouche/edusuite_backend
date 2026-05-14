from dataclasses import dataclass
from uuid import UUID
from datetime import date, time
from src.features.training.enums.session import SessionOccurenceState


@dataclass
class SessionOccurence:
    session_id: UUID
    planned_date: date
    start_at: time
    end_at: time
    status: SessionOccurenceState
    notes: str

    id: UUID | None = None
