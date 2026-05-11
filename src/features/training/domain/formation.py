from src.features.training.enums.formation_enums import (
    TypeFormation,
    StatusFormation,
    NiveauFormation,
    DomainFormation,
)
from src.features.training.domain.module import Module
from dataclasses import dataclass
from uuid import UUID


@dataclass
class FormationList:
    id: UUID
    type: TypeFormation
    niveau: NiveauFormation
    status: StatusFormation
    titre: str
    domaine: DomainFormation

    @staticmethod
    def to_domain(orm):
        return FormationList(
            id=orm.id,
            type=orm.type,
            niveau=orm.niveau,
            status=orm.status,
            titre=orm.titre,
            domaine=orm.domaine,
        )


@dataclass
class Formation:
    """
    TOO MUCH DATA PACKED HERE
    """

    titre: str
    code: str
    duree_jours: int
    heures_par_jour: int
    certifiante: bool

    domaine: DomainFormation
    id: UUID | None = None
    prix: float | None = None
    description: str | None = None
    type: TypeFormation | None = None
    niveau: NiveauFormation | None = None
    status: StatusFormation | None = None
    modules: list[Module] | None = None

    @staticmethod
    def to_domain(orm, modules: list[Module] | None = None):
        return Formation(
            modules=modules,
            titre=orm.titre,
            heures_par_jour=orm.heures_par_jour,
            code=orm.code,
            duree_jours=orm.duree_jours,
            certifiante=orm.certifiante,
            domaine=orm.domaine,
            id=orm.id,
            prix=orm.prix,
            description=orm.description,
            type=orm.type,
            niveau=orm.niveau,
            status=orm.status,
        )
