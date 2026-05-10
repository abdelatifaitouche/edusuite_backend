import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, UUID
from src.db.base import Base


class Module(Base):
    __tablename__ = "modules"

    formation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("formations.id"), nullable=True
    )
    titre: Mapped[str] = mapped_column(String, nullable=False)
    contenu: Mapped[str] = mapped_column(String, nullable=True)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    durée_heure: Mapped[int] = mapped_column(Integer, nullable=True, default=1)

    formation: Mapped["Formation"] = relationship("Formation", back_populates="modules")

    def __repr__(self):
        return f"Module<{self.titre}>"
