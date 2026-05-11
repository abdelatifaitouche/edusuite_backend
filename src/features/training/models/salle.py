from src.db.base import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, String, Enum, Integer, Boolean, Numeric
from src.features.training.enums.salle import SalleState


class Salle(Base):
    __tablename__ = "salles"

    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    status: Mapped[SalleState] = mapped_column(
        Enum(SalleState), default=SalleState.DISPONIBLE
    )
    size: Mapped[int] = mapped_column(Integer, nullable=True, default=0)

    def __repr__(self):
        return f"Salle<{self.name}> --- Status {self.status} --- size {self.size}"
