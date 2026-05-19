from dataclasses import dataclass
from enum import StrEnum
from datetime import date, time
from uuid import UUID
from src.features.training.enums.session import (
    PlanningType,
    SessionState,
)


@dataclass
class Session:
    formation_id: UUID
    formateur_id: UUID
    start_date: date
    end_date: date
    salle_id: UUID
    type_planinng: PlanningType
    status: SessionState | None = None
    session_number: str | None = None
    id: UUID | None = None
