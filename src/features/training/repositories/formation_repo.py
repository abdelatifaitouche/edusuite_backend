from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from uuid import UUID

from src.db.repositories.base_repository import BaseRepository
from src.features.training.models.formation import Formation as FormationDB
from src.features.training.domain.formation import Formation as FormationEntity
from src.features.training.domain.module import Module as ModuleEntity


class FormationRepo(BaseRepository[FormationEntity, FormationDB]):
    model = FormationDB

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_formation_details(self, entity_id: UUID):

        stmt = (
            select(FormationDB)
            .where(FormationDB.id == entity_id)
            .options(selectinload(FormationDB.modules))
        )

        result = await self.db.execute(stmt)
        formation = result.scalar_one_or_none()

        if not formation:
            return

        modules = [ModuleEntity.to_domain(module) for module in formation.modules]

        return

    def _to_domain(self, orm: FormationDB) -> FormationEntity:
        return FormationEntity(
            titre=orm.titre,
            code=orm.code,
            description=orm.description,
            type=orm.type,
            id=orm.id,
            niveau=orm.niveau,
            status=orm.status,
            domaine=orm.domaine,
            duree_jours=orm.duree_jours,
            heures_par_jour=orm.heures_par_jour,
            prix=orm.prix,
            certifiante=orm.certifiante,
        )

    def _to_orm(self, entity: FormationEntity) -> FormationDB:
        return FormationDB(
            titre=entity.titre,
            code=entity.code,
            description=entity.description,
            type=entity.type,
            id=entity.id,
            niveau=entity.niveau,
            status=entity.status,
            domaine=entity.domaine,
            duree_jours=entity.duree_jours,
            heures_par_jour=entity.heures_par_jour,
            prix=entity.prix,
            certifiante=entity.certifiante,
        )
