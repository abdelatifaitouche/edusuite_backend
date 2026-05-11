from src.db.usecases.base_usecase import BaseUC
from src.features.training.repositories.salle_repo import SalleRepository
from src.features.training.schemas.salle import SalleCreate, SalleRead, SalleUpdate
from src.features.training.domain.salle import Salle as SalleEntity


class SalleUC(BaseUC[SalleEntity, SalleCreate, SalleUpdate]):
    def __init__(self, repo: SalleRepository):
        super().__init__(repo)
        self.repo = repo

    def _to_entity(self, data: SalleCreate) -> SalleEntity:
        return SalleEntity(name=data.name, size=data.size, status=data.status)

    async def _apply_update(
        self, entity: SalleEntity, data: SalleUpdate
    ) -> SalleEntity:

        if data.status:
            entity.status = data.status

        if data.size:
            entity.size = data.size

        if data.name:
            entity.name = data.name

        return entity
