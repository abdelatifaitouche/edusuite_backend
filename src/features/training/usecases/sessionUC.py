from src.db.usecases.base_usecase import BaseUC
from src.features.training.repositories.session_repo import SessionRepository
from src.features.training.schemas.session import CreateSession
from src.features.training.enums.session import PlanningType
from src.features.training.domain.session import (
    Session as SessionEntity,
)
from src.features.training.repositories.reccurrence_repo import ReccurenceRepository


class SessionUC(BaseUC[SessionEntity, CreateSession, CreateSession]):
    def __init__(self, repo: SessionRepository):
        super().__init__(repo)
        self.repo = repo
        self.rrule_repo = ReccurenceRepository(self.repo.db)

    def _to_entity(self, data: CreateSession):
        return SessionEntity(
            formation_id=data.formation_id,
            formateur_id=data.formateur_id,
            salle_id=data.salle_id,
            start_date=data.date_debut,
            end_date=data.date_fin,
            type_planinng=data.type_planning,
        )

    async def create_session(self, data: CreateSession) -> SessionEntity:
        # before creating session we should first check for formateur availablity, and salle availilibity
        # so we should fetch occurences
        session: SessionEntity = await self.repo.save(self._to_entity(data))

        if not session:
            raise Exception("Session was not created")

        return session
