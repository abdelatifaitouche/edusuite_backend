from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db


from src.features.training.schemas.session import CreateSession
from src.features.training.orchestrators.session_orchestrator import SessionOrchestrator
from src.features.training.usecases.sessionUC import SessionUC
from src.features.training.repositories.session_repo import SessionRepository
from src.features.training.repositories.reccurrence_repo import ReccurenceRepository
from src.features.training.usecases.reccurrence_ruleUC import RRuleUC
from src.features.training.repositories.occurrence_repo import OccurrenceRepository
from src.core.exception import SessionConflictError

router = APIRouter(prefix="/sessions")


def get_orchestrator(db: AsyncSession = Depends(get_db)):
    s_repo = SessionRepository(db)
    r_repo = ReccurenceRepository(db)
    s_occ_repo = OccurrenceRepository(db)
    s_service = SessionUC(s_repo)
    r_service = RRuleUC(r_repo)
    return SessionOrchestrator(s_service, r_service, s_occ_repo)


@router.post("/")
async def create_session(
    data: CreateSession, orch: SessionOrchestrator = Depends(get_orchestrator)
):
    session = await orch.create_session(data)
    return session
