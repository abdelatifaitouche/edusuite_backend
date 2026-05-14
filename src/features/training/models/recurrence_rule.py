from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UUID, String, Integer, Time
from sqlalchemy.dialects.postgresql import ARRAY
import uuid
from src.db.base import Base
from datetime import time


class RecurrenceRule(Base):
    __tablename__ = "recurrence_rules"

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("sessions.id"),
        nullable=False,
        unique=True,
    )
    days_week: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False)
    start_at: Mapped[time] = mapped_column(Time, nullable=False)
    ends_at: Mapped[time] = mapped_column(Time, nullable=False)
    week_interval: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    session: Mapped["Session"] = relationship(
        "Session", back_populates="recurrence_rule"
    )
