from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories.base_repository import BaseRepository
from src.features.training.models.formateur import Formateur as FormateurDB
from src.features.training.domain.formateur import Formateur as FormateurEntity
from src.features.training.filters.formateur_filters import FormateurFilters


class FormateurRepo(BaseRepository[FormateurEntity, FormateurDB]):
    model = FormateurDB

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    def _apply_filters(self, stmt, filters: FormateurFilters):

        if filters.status:
            stmt = stmt.where(self.model.status == filters.status)

        return stmt

    def _to_domain(self, orm: FormateurDB) -> FormateurEntity:
        return FormateurEntity(
            prenom=orm.prenom,
            nom=orm.nom,
            email=orm.email,
            telephone=orm.telephone,
            id=orm.id,
            niveau_expertise=orm.niveau_expertise,
            status=orm.status,
            cv_url=orm.cv_url,
            specialite=orm.specialite,
            bio=orm.bio,
            year_of_experience=orm.year_of_experience,
            ville=orm.ville,
            daily_rate=orm.daily_rate,
        )

    def _to_orm(self, entity: FormateurEntity) -> FormateurDB:
        return FormateurDB(
            id=entity.id,
            nom=entity.nom,
            prenom=entity.prenom,
            email=entity.email,
            telephone=entity.telephone,
            niveau_expertise=entity.niveau_expertise,
            specialite=entity.specialite,
            status=entity.status,
            cv_url=entity.cv_url,
            bio=entity.bio,
            daily_rate=entity.daily_rate,
            year_of_experience=entity.year_of_experience,
            ville=entity.ville,
        )

    async def _orm_update(
        self,
        orm: FormateurDB,
        entity: FormateurEntity,
    ) -> FormateurDB:

        if entity.status:
            orm.status = entity.status
        return orm
