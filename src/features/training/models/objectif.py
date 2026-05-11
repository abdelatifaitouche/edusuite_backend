from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, UUID, ForeignKey
import uuid
from src.db.base import Base


class Objectif(Base):
    __tablename__ = "objectifs"

    titre: Mapped[str] = mapped_column(String, nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    formation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("formations.id"),
        nullable=False,
    )

    formation: Mapped["Formation"] = relationship(
        "Formation", back_populates="objectifs"
    )

    def __repr__(self):
        return f"Objectif : {self.titre}"
