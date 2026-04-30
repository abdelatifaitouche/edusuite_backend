from enum import StrEnum
from uuid import UUID
from src.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum
from src.features.crm.enums.sessionplan_state import SessionPlanStatus, LocationType


class SessionPlan(Base):
    __tablename__ = "sessionplans"
    opportunity_id: Mapped[UUID] = mapped_column(
        ForeignKey("opportunities.id", ondelete="CASCADE"),
        unique=True,  # one-to-one relationship
    )
    status: Mapped[SessionPlanStatus] = mapped_column(
        Enum(SessionPlanStatus), default=SessionPlanStatus.DRAFT, nullable=False
    )
    expected_students: Mapped[int] = mapped_column(nullable=False)

    location_type: Mapped[LocationType] = mapped_column(
        Enum(LocationType), nullable=False
    )
    venue_cost: Mapped[float] = mapped_column(nullable=False, default=0.0)

    cost_per_student: Mapped[float] = mapped_column(nullable=False, default=0.0)

    # Relationship
    opportunity: Mapped["Opportunity"] = relationship(back_populates="session_plan")
