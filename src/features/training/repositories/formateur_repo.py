from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import join, select
from sqlalchemy.orm import selectinload
from uuid import UUID
from src.db.repositories.base_repository import BaseRepository
from src.features.training.models.formateur import Formateur as FormateurDB
from src.features.training.domain.formateur import (
    Formateur as FormateurEntity,
    BaseFormateur as FormateurSummary,
)
from src.features.training.filters.formateur_filters import FormateurFilters
from src.features.training.models.formation_formateur import FormateurFormation
from src.features.training.models.formation import Formation as FormationDB
from src.features.training.repositories.formation_repo import FormationRepo

from src.features.training.domain.formateur import ReadCourseMini


class FormateurRepo(BaseRepository[FormateurEntity, FormateurDB]):
    model = FormateurDB

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    def _apply_filters(self, stmt, filters: FormateurFilters):

        if filters.status:
            stmt = stmt.where(self.model.status == filters.status)

        if filters.specialite:
            stmt = stmt.where(self.model.specialite == filters.specialite)

        return stmt

    async def get_trainer_details(self, trainer_id: UUID):
        stmt = (
            select(FormateurDB)
            .options(
                selectinload(FormateurDB.formations).selectinload(
                    FormateurFormation.formation
                )
            )
            .where(FormateurDB.id == trainer_id)
        )

        result = await self.db.scalar(stmt)
        if not result:
            raise
        courses = [
            ReadCourseMini(c.formation.id, c.formation.titre) for c in result.formations
        ]

        return self._to_domain(result, courses)

    async def assign_course(self, trainer_id: UUID, course_id: UUID):
        link = FormateurFormation(formation_id=course_id, formateur_id=trainer_id)

        self.db.add(link)

        await self.db.flush()

        return True

    async def get_trainer_courses(self, trainer_id: UUID):

        formation_repo: FormationRepo = FormationRepo(self.db)

        stmt = (
            select(FormationDB)
            .join(FormateurFormation, FormateurFormation.formation_id == FormationDB.id)
            .where(FormateurFormation.formateur_id == trainer_id)
        )

        result = await self.db.scalars(stmt)

        models = result.all()

        return [formation_repo._to_domain(model) for model in models]

    async def list_trainers(
        self, pagination, filters: FormateurFilters
    ) -> list[FormateurSummary]:
        stmt = select(FormateurDB)
        stmt = self._apply_filters(stmt, filters)
        stmt = self._apply_pagination(stmt, pagination)
        results = await self.db.execute(stmt)

        trainers = results.scalars()

        return [self._to_summary(trainer) for trainer in trainers]

    def _to_summary(self, orm: FormateurDB):
        return FormateurSummary(
            id=orm.id,
            nom=orm.nom,
            prenom=orm.prenom,
            email=orm.email,
            telephone=orm.telephone,
            specialite=orm.specialite,
            status=orm.status,
        )

    def _to_domain(self, orm: FormateurDB, courses=None) -> FormateurEntity:
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
            courses=courses if courses else None,
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

        if entity.daily_rate:
            orm.daily_rate = entity.daily_rate

        if entity.year_of_experience:
            orm.year_of_experience = entity.year_of_experience

        if entity.ville:
            orm.ville = entity.ville

        if entity.status:
            orm.status = entity.status
        return orm
