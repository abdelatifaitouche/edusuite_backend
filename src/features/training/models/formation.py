from src.db.base import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, String, Enum, Integer, Boolean, Numeric

from src.features.training.enums.formation_enums import (
    DomainFormation,
    NiveauFormation,
    TypeFormation,
    StatusFormation,
)

from typing import Optional, List


class Formation(Base):
    """Training program / course definition."""

    __tablename__ = "formations"

    titre: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    domaine: Mapped[DomainFormation] = mapped_column(
        Enum(DomainFormation), nullable=False
    )
    type: Mapped[TypeFormation] = mapped_column(Enum(TypeFormation), nullable=False)
    niveau: Mapped[NiveauFormation] = mapped_column(
        Enum(NiveauFormation), default=NiveauFormation.tous_niveaux, nullable=False
    )
    duree_jours: Mapped[int] = mapped_column(Integer, nullable=False)
    heures_par_jour: Mapped[int] = mapped_column(Integer, default=6, nullable=False)
    prix: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)
    certifiante: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    status: Mapped[Optional[StatusFormation]] = mapped_column(
        Enum(StatusFormation), default=StatusFormation.DISPONIBLE
    )

    # relationships
    formateurs: Mapped[List["FormateurFormation"]] = relationship(
        "FormateurFormation", back_populates="formation", cascade="all, delete-orphan"
    )

    modules = relationship(
        "Module", back_populates="formation", cascade="all, delete-orphan"
    )

    objectifs = relationship(
        "Objectif", back_populates="formation", cascade="all, delete-orphan"
    )

    @property
    def duree_totale_heures(self) -> int:
        return self.duree_jours * self.heures_par_jour

    def __repr__(self) -> str:
        return f"<Formation {self.code!r} — {self.titre!r}>"
