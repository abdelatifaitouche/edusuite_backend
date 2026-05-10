from uuid import UUID
from dataclasses import dataclass


@dataclass
class Module:
    titre: str
    contenu: str
    order: int
    durée_heure: int
    id: UUID | None = None
    formation_id: UUID | None = None

    @classmethod
    def to_domain(cls, orm):
        return Module(
            id=orm.id,
            titre=orm.titre,
            contenu=orm.contenu,
            durée_heure=orm.durée_heure,
            order=orm.order,
            formation_id=orm.formation_id,
        )
