from src.db.base import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, UUID, UniqueConstraint, func, ForeignKey, DateTime

import uuid
from datetime import datetime
from src.features.training.enums.formateur_enums import RoleFormateur


class FormateurFormation(Base):
    """
    Pivot table for the many-to-many relationship between
    Formateur and Formation. Carries the role of the trainer
    within that specific formation.
    """

    __tablename__ = "formateur_formations"
    __table_args__ = (
        UniqueConstraint("formateur_id", "formation_id", name="uq_formateur_formation"),
    )

    formateur_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("formateurs.id", ondelete="CASCADE"),
        nullable=False,
    )
    formation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("formations.id", ondelete="CASCADE"),
        nullable=False,
    )
    role: Mapped[RoleFormateur] = mapped_column(
        Enum(RoleFormateur), default=RoleFormateur.principal, nullable=False
    )
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # relationships
    formateur: Mapped["Formateur"] = relationship(
        "Formateur", back_populates="formations"
    )
    formation: Mapped["Formation"] = relationship(
        "Formation", back_populates="formateurs"
    )

    def __repr__(self) -> str:
        return f"<FormateurFormation formateur={self.formateur_id} formation={self.formation_id} role={self.role}>"
