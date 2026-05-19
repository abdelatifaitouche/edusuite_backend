from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, UUID, ForeignKey, DateTime, Enum, Time
from datetime import date as dd, time
import uuid
from src.db.base import Base
from src.features.training.enums.session import SessionOccurenceState


class SessionOccurrence(Base):
    __tablename__ = "sessions_occurrences"

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sessions.id"),
        nullable=False,
    )
    date: Mapped[dd] = mapped_column(DateTime, nullable=False)
    start_at: Mapped[time] = mapped_column(Time, nullable=False)
    end_at: Mapped[time] = mapped_column(Time, nullable=False)
    status: Mapped[SessionOccurenceState] = mapped_column(
        Enum(SessionOccurenceState),
        default=SessionOccurenceState.DRAFT,
    )
    note: Mapped[str] = mapped_column(String, nullable=True)

    session = relationship("Session", back_populates="session_occurence")
