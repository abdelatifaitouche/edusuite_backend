from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories.base_repository import BaseRepository
from src.features.training.models.modules import Module as ModuleDB
from src.features.training.domain.module import Module as ModuleEntity


class ModuleRepository(BaseRepository[ModuleEntity, ModuleDB]):
    model = ModuleDB

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    def _to_domain(self, orm: ModuleDB) -> ModuleEntity:
        return ModuleEntity(
            id=orm.id,
            titre=orm.titre,
            order=orm.order,
            formation_id=orm.formation_id,
            contenu=orm.contenu,
            durée_heure=orm.durée_heure,
        )

    def _to_orm(self, entity: ModuleEntity) -> ModuleDB:
        return ModuleDB(
            titre=entity.titre,
            order=entity.order,
            formation_id=entity.formation_id,
            contenu=entity.contenu,
            durée_heure=entity.durée_heure,
        )
