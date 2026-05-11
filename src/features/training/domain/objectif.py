from dataclasses import dataclass
from uuid import UUID
from src.features.training.models.objectif import Objectif as ObjectifDB


@dataclass
class Objectif:
    titre: str
    order: int

    id: UUID | None = None
    formation_id: UUID | None = None

    @staticmethod
    def to_domain(orm: ObjectifDB):
        return Objectif(
            id=orm.id,
            order=orm.order,
            formation_id=orm.formation_id,
            titre=orm.titre,
        )
