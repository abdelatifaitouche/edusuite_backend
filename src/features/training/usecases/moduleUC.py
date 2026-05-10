from src.db.usecases.base_usecase import BaseUC
from src.features.training.schemas.module import ModuleCreate, ModuleRead, ModuleUpdate
from src.features.training.domain.module import Module as ModuleEntity
from src.features.training.repositories.module_repo import ModuleRepository


class ModuleUC(BaseUC[ModuleEntity, ModuleCreate, ModuleRead]):
    def __init__(self, repo: ModuleRepository):
        super().__init__(repo=repo)
        self.repo = repo

    def _to_entity(self, data: ModuleCreate) -> ModuleEntity:
        return ModuleEntity(
            titre=data.titre,
            durée_heure=data.durée_heure,
            order=data.order,
            contenu=data.contenu,
            formation_id=data.formation_id,
        )
