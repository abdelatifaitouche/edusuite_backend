from datetime import datetime, date

from src.db.base import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum, Date, Integer, Numeric
from typing import Optional

from src.features.crm.enums.opportunity_states import OpportunityStates


class Opportunity(Base):
    __tablename__ = "opportunities"

    title: Mapped[str] = mapped_column(String, nullable=False)

    status: Mapped[OpportunityStates] = mapped_column(
        Enum(OpportunityStates, name="opportunity_states"),
        nullable=False,
        default=OpportunityStates.NEW,
        index=True,
    )

    estimated_value: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    probability: Mapped[int] = mapped_column(Integer, nullable=False)  # 0–100

    expected_close_date: Mapped[date] = mapped_column(Date, nullable=False)

    session_plan: Mapped[Optional["SessionPlan"]] = relationship(
        back_populates="opportunity", uselist=False, cascade="all, delete-orphan"
    )
