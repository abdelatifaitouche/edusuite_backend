from uuid import UUID


from src.db.usecases.base_usecase import BaseUC
from src.features.training.repositories.formation_repo import FormationRepo
from src.features.training.domain.formation import (
    Formation as FormationEntity,
    FormationList,
)
from src.features.training.schemas.formation import CreateFormation, ReadFormation
from src.core.pagination import Pagination
from src.features.training.filters.formation_filters import FormationFilters


class FormationUC(BaseUC[FormationEntity, CreateFormation, ReadFormation]):
    def __init__(self, repo: FormationRepo):
        super().__init__(repo=repo)
        self.repo: FormationRepo = repo

    async def get_by_id(self, entity_id: UUID) -> FormationEntity:
        result = await self.repo.get_formation_details(entity_id)
        return result

    async def list(
        self, pagination: Pagination, filters: FormationFilters
    ) -> list[FormationList]:

        results = await self.repo.list_formation(pagination, filters)

        return results

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
