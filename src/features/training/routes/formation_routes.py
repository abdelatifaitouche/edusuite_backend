from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from src.db.session import get_db
from src.core.pagination import Pagination
from src.features.training.repositories.formation_repo import FormationRepo
from src.features.training.usecases.formationUC import FormationUC
from src.features.training.schemas.formation import CreateFormation, ReadFormation

router = APIRouter(prefix="/courses")


def get_repo(db: AsyncSession = Depends(get_db)):
    return FormationRepo(db)


def get_service(repo: FormationRepo = Depends(get_repo)):
    return FormationUC(repo)


@router.post("")
async def create_course(
    data: CreateFormation,
    uc: FormationUC = Depends(get_service),
):
    course = await uc.create(data)
    return ReadFormation.model_validate(course)


@router.get("")
async def list_courses(
    pagination: Pagination = Depends(),
    uc: FormationUC = Depends(get_service),
):
    courses = await uc.list(pagination)
    return [ReadFormation.model_validate(course) for course in courses]


@router.get("/{course_id}")
async def get_course(
    course_id: str,
    uc: FormationUC = Depends(get_service),
):
    course = await uc.get_by_id(UUID(course_id))
    return ReadFormation.model_validate(course)


@router.delete("/{course_id}")
async def delete_course(
    course_id: str,
    uc: FormationUC = Depends(get_service),
):
    status = await uc.delete(UUID(course_id))
    return status
