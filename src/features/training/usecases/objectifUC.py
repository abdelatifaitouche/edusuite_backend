from src.db.usecases.base_usecase import BaseUC
from src.features.training.domain.objectif import Objectif as ObjectifEntity
from src.features.training.schemas.objectif import (
    ObjectifRead,
    ObjectifUpdate,
    ObjectifCreate,
)
from src.features.training.repositories.objectif_repo import ObjectifRepository
from uuid import UUID


class ObjectifUC(BaseUC[ObjectifEntity, ObjectifCreate, ObjectifRead]):
    def __init__(self, repo: ObjectifRepository):
        super().__init__(repo)
        self.repo = repo

    def _to_entity(self, data: ObjectifCreate) -> ObjectifEntity:
        return ObjectifEntity(
            titre=data.titre,
            order=data.order,
        )

    async def get_course_objectif(self, course_id: UUID) -> list[ObjectifEntity]:
        results = await self.repo.get_course_objectifs(course_id)
        return results

    async def create_objectif(self, data: ObjectifCreate, formation_id: UUID):

        if data.order <= 0:
            raise Exception("Invalid Order for objectif")

        entity = ObjectifEntity(
            titre=data.titre,
            formation_id=formation_id,
            order=data.order,
        )

        return await self.repo.save(entity)
