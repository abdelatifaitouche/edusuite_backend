from src.db.base import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, String, Boolean, Enum
from src.features.training.enums.formateur_enums import NiveauExpertise, FormateurStatus
from src.features.training.enums.formation_enums import DomainFormation

from typing import Optional, List


class Formateur(Base):
    """Trainer / instructor profile."""

    __tablename__ = "formateurs"

    prenom: Mapped[str] = mapped_column(String(100), nullable=False)
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    telephone: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)

    specialite: Mapped[Optional[DomainFormation]] = mapped_column(
        Enum(DomainFormation), nullable=True
    )
    niveau_expertise: Mapped[Optional[NiveauExpertise]] = mapped_column(
        Enum(NiveauExpertise), nullable=True
    )
    cv_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[Optional[FormateurStatus]] = mapped_column(
        Enum(FormateurStatus),
        default=FormateurStatus.ACTIVE,
    )
    # relationships
    formations: Mapped[List["FormateurFormation"]] = relationship(
        "FormateurFormation", back_populates="formateur", cascade="all, delete-orphan"
    )

    @property
    def full_name(self) -> str:
        return f"{self.prenom} {self.nom}"

    def __repr__(self) -> str:
        return f"<Formateur {self.full_name!r}>"
