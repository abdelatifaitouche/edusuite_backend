from uuid import UUID


from src.db.usecases.base_usecase import BaseUC
from src.features.training.repositories.formation_repo import FormationRepo
from src.features.training.domain.formation import Formation as FormationEntity
from src.features.training.schemas.formation import CreateFormation, ReadFormation


class FormationUC(BaseUC[FormationEntity, CreateFormation, ReadFormation]):
    def __init__(self, repo: FormationRepo):
        super().__init__(repo=repo)
        self.repo: FormationRepo = repo

    def _to_entity(self, data: CreateFormation):
        return FormationEntity(
            titre=data.titre,
            code=data.titre,
            description=data.description,
            duree_jours=data.duree_jours,
            heures_par_jour=data.heures_par_jour,
            type=data.type,
            prix=data.prix,
            niveau=data.niveau,
            domaine=data.domaine,
            status=data.status,
            certifiante=data.certifiante,
        )
