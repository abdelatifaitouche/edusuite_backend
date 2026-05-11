from fastapi import APIRouter, Depends
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db
from src.features.training.repositories.objectif_repo import ObjectifRepository
from src.features.training.usecases.objectifUC import ObjectifUC
from src.features.training.schemas.objectif import ObjectifCreate, ObjectifRead

router = APIRouter(prefix="/formations/{formation_id}/objectifs")


def get_repo(db: AsyncSession = Depends(get_db)):
    return ObjectifRepository(db)


def get_service(repo: ObjectifRepository = Depends(get_repo)):
    return ObjectifUC(repo)


@router.get("")
async def list_course_objectif(
    formation_id: str,
    uc: ObjectifUC = Depends(get_service),
):
    results = await uc.get_course_objectif(UUID(formation_id))
    return [ObjectifRead.model_validate(obj) for obj in results]


@router.post("/")
async def add_objectif(
    formation_id: str,
    data: ObjectifCreate,
    uc: ObjectifUC = Depends(get_service),
):
    result = await uc.create_objectif(data, UUID(formation_id))
    return ObjectifRead.model_validate(result)


@router.delete("/{objectif_id}/")
async def remove_objectif(
    formation_id: str,
    objectif_id: str,
    uc: ObjectifUC = Depends(get_service),
):
    result = await uc.delete(UUID(objectif_id))
    return result
