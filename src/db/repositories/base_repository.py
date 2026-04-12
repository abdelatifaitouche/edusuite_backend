from src.db.base import Base
from collections.abc import Sequence
from typing import TypeVar, Type, Generic
from src.core.pagination import Pagination
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from uuid import UUID

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """ """

    def __init__(self, db: AsyncSession, model: Type[ModelType]):
        self.model: Type[ModelType] = model
        self.db: AsyncSession = db

    async def list(self, pagination: Pagination) -> list[ModelType]:
        stmt = select(self.model).offset(pagination.offset).limit(pagination.page_size)
        results = await self.db.execute(stmt)
        data = results.scalars().all()
        return data

    async def save(self, data: ModelType) -> ModelType:
        self.db.add(data)
        await self.db.flush()
        return data

    async def get_by_id(self, entity_id: UUID) -> ModelType:
        return

    async def update(self):
        return

    async def delete(self):
        return
