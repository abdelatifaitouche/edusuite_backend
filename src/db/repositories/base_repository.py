from src.db.base import Base
from collections.abc import Sequence
from typing import TypeVar, Type, Generic
from src.core.pagination import Pagination
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """ """

    def __init__(self, model: Type[ModelType]):
        self.model: Type[ModelType] = model

    async def list(
        self, db: AsyncSession, pagination: Pagination
    ) -> Sequence[ModelType]:
        stmt = select(self.model).offset(pagination.offset).limit(pagination.page_size)
        results = await db.execute(stmt)
        data = results.scalars().all()
        return data

    async def save(self):
        return

    async def get_by_id(self):
        return

    async def update(self):
        return

    async def delete(self):
        return
