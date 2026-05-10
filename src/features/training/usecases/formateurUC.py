from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from src.features.training.repositories.formateur_repo import FormateurRepo
from src.db.usecases.base_usecase import BaseUC
from src.features.training.domain.formateur import (
    Formateur as FormateurEntity,
    BaseFormateur as FormateurSummary,
)
from src.features.training.schemas.formateur import FormateurCreate, FormateurUpdate
from src.features.training.enums.formateur_enums import FormateurStatus

from src.features.training.repositories.formation_repo import FormationRepo


class FormateurUC(BaseUC[FormateurEntity, FormateurCreate, FormateurUpdate]):
    def __init__(self, repo: FormateurRepo):
        super().__init__(repo=repo)
        self.repo: FormateurRepo = repo

    def _to_entity(self, data: FormateurCreate) -> FormateurEntity:
        return FormateurEntity(
            email=data.email,
            prenom=data.prenom,
            nom=data.nom,
            specialite=data.specialite,
            telephone=data.telephone,
            year_of_experience=data.year_of_experience,
            ville=data.ville,
            daily_rate=data.daily_rate,
        )

    async def list_trainers(self, pagination, filters) -> list[FormateurSummary]:
        trainers = await self.repo.list_trainers(pagination, filters)
        return trainers

    async def get_details(self, trainer_id: UUID):
        trainer = await self.repo.get_trainer_details(trainer_id)
        return trainer

    async def add_course_to_trainer(self, trainer_id: UUID, course_id: UUID):

        formation_repo: FormationRepo = FormationRepo(self.repo.db)

        trainer = await self.get_by_id(trainer_id)

        course = await formation_repo.get_by_id(course_id)

        if not course:
            raise Exception("Course Not Found")

        return await self.repo.assign_course(trainer_id, course_id)

    async def get_trainer_courses(self, trainer_id: UUID):

        trainer = await self.get_by_id(trainer_id)

        courses = await self.repo.get_trainer_courses(trainer_id)

        return courses

    async def block_trainer(self, trainer_id: UUID):
        trainer: FormateurEntity = await self.get_by_id(trainer_id)

        if trainer.status != FormateurStatus.ACTIVE:
            return

        trainer.status = FormateurStatus.NON_ACTIVE

        updated_trainer = await self.repo.save(trainer)

        return updated_trainer

    async def _apply_update(
        self, entity: FormateurEntity, data: FormateurUpdate
    ) -> FormateurEntity:

        if data.daily_rate:
            entity.daily_rate = data.daily_rate

        if data.ville:
            entity.ville = data.ville

        if data.year_of_experience:
            entity.year_of_experience = data.year_of_experience

        return entity
