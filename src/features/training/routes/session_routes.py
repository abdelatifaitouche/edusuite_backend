from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db
from uuid import UUID

from src.features.training.schemas.session import CreateSession, ReadSession
from src.features.training.orchestrators.session_orchestrator import SessionOrchestrator
from src.features.training.usecases.sessionUC import SessionUC
from src.features.training.repositories.session_repo import SessionRepository
from src.features.training.repositories.reccurrence_repo import ReccurenceRepository
from src.features.training.usecases.reccurrence_ruleUC import RRuleUC
from src.features.training.repositories.occurrence_repo import OccurrenceRepository
from src.core.exception import SessionConflictError
from src.core.filters import BaseFilters
from src.core.pagination import Pagination
from src.features.training.schemas.session_occurrences import ReadOccurrence


router = APIRouter(prefix="/sessions")


def get_repo(db: AsyncSession = Depends(get_db)):
    return SessionRepository(db)


def get_service(repo: SessionRepository = Depends(get_repo)):
    return SessionUC(repo)


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


@router.patch("/{session_id}/cancel/")
async def cancel_session(
    session_id: str, orch: SessionOrchestrator = Depends(get_orchestrator)
):
    session = await orch.cancel_session(UUID(session_id))
    return ReadSession.model_validate(session)


@router.get("/")
async def list_sessions(
    pagination: Pagination = Depends(),
    filters: BaseFilters = Depends(),
    uc: SessionUC = Depends(get_service),
):
    results = await uc.list(pagination, filters)
    return [ReadSession.model_validate(ses) for ses in results]


@router.get("/{session_id}/occurrences")
async def get_session_occurrences(
    session_id: str,
    orch: SessionOrchestrator = Depends(get_orchestrator),
):
    results = await orch.get_session_occurrences(UUID(session_id))
    return [ReadOccurrence.model_validate(res) for res in results]
