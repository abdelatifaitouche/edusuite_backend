from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, String, Integer, ForeignKey, Enum, DateTime
import uuid

from src.db.base import Base
from src.features.training.enums.session import PlanningType, SessionState
from datetime import datetime


class Session(Base):
    __tablename__ = "sessions"

    formation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("formations.id"),
        nullable=False,
    )
    formateur_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("formateurs.id"),
        nullable=False,
    )
    salle_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("salles.id"),
        nullable=False,
    )
    status: Mapped[SessionState] = mapped_column(
        Enum(SessionState),
        default=SessionState.DRAFT,
    )
    planning_type: Mapped[PlanningType] = mapped_column(
        Enum(PlanningType),
        default=PlanningType.BLOC,
    )
    date_debut: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    date_fin: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    formation: Mapped["Formation"] = relationship(
        "Formation", back_populates="sessions"
    )

    formateur: Mapped["Formateur"] = relationship(
        "Formateur", back_populates="sessions"
    )

    salle: Mapped["Salle"] = relationship(
        "Salle",
        back_populates="sessions",
    )

    recurrence_rule = relationship(
        "RecurrenceRule",
        back_populates="session",
        uselist=False,
    )

    session_occurence = relationship("SessionOccurrence", back_populates="session")
