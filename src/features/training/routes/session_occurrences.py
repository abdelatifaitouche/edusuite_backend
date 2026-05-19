from fastapi import APIRouter, Depends
from src.features.training.filters.session_occurrences import OccurrenceFilters
from src.features.training.repositories.occurrence_repo import OccurrenceRepository
from src.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.pagination import Pagination
from src.features.training.schemas.session_occurrences import OccurrenceCompact

router = APIRouter(prefix="/occurrences")


def get_repo(db: AsyncSession = Depends(get_db)):
    return OccurrenceRepository(db)


@router.get("")
async def list_occurrences(
    pagination: Pagination = Depends(),
    filters: OccurrenceFilters = Depends(),
    repo: OccurrenceRepository = Depends(get_repo),
):
    oc = await repo.list_calendar(pagination, filters)

    return [OccurrenceCompact.model_validate(o) for o in oc]
