from dataclasses import dataclass
from enum import StrEnum
from datetime import date, time
from uuid import UUID
from src.features.training.enums.session import (
    PlanningType,
    SessionState,
)
from src.features.training.domain.session_occurrence import SessionOccurence


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


@dataclass
class SessionDetails:
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
    occurrences: list[SessionOccurence]
