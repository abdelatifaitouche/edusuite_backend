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

    @staticmethod
    def to_domain(orm):
        return SessionOccurence(
            session_id=orm.session_id,
            planned_date=orm.date,
            start_at=orm.start_at,
            end_at=orm.end_at,
            status=orm.status,
            notes=orm.note,
            id=orm.id,
        )


@dataclass
class SessionOccurrenceCompact:
    session_number: str
    session_id: UUID
    formateur_name: str
    formation_name: str
    planned_date: date
    start_at: time
    end_date: time
    status: SessionOccurenceState
    id: UUID


@dataclass
class ConflictResult:
    conflicting_dates: list[date]
    formateur_conflict: bool
    salle_conflict: bool
