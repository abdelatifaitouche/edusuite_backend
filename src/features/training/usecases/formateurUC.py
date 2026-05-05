from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from src.features.training.repositories.formateur_repo import FormateurRepo
from src.db.usecases.base_usecase import BaseUC
from src.features.training.domain.formateur import Formateur as FormateurEntity
from src.features.training.schemas.formateur import FormateurCreate, FormateurUpdate
from src.features.training.enums.formateur_enums import FormateurStatus


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

        if data.status:
            entity.status = data.status

        return entity
