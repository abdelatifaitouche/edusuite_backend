from src.db.base import Base
from collections.abc import Sequence
from typing import TypeVar, Type, Generic
from src.core.pagination import Pagination
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from uuid import UUID
from src.core.request_context import RequestContext

from abc import ABC

T = TypeVar("T")
M = TypeVar("M")


class BaseRepository(ABC, Generic[T, M]):
    model: type[M]

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    def _apply_pagination(self, stmt, pagination: Pagination):
        return stmt.offset(pagination.offset).limit(pagination.page_size)

    def _apply_filters(self, stmt):
        """
        gets base filters
        """
        return stmt

    def _to_orm(self, entity: T) -> M:
        """
        Converts the domain object into the ORM model
        """
        raise NotImplementedError()

    def _to_domain(self, orm: M) -> T:
        """
        Converts the ORM model into the domain model
        """
        raise NotImplementedError()

    async def list(self, pagination: Pagination, filters=None) -> list[T]:
        stmt = select(self.model)

        # apply filters
        stmt = self._apply_filters(stmt)
        # apply pagination
        stmt = self._apply_pagination(stmt, pagination)
        results = await self.db.execute(stmt)
        data: list[M] = results.scalars().all()
        return [self._to_domain(row) for row in data]

    async def save(self, data: T) -> T:
        orm = self._to_orm(data)

        self.db.add(orm)
        await self.db.flush()
        return self._to_domain(orm)

    async def get_by_id(self, entity_id: UUID) -> T | None:

        orm = await self.db.get(self.model, entity_id)

        return self._to_domain(orm) if orm else None

    async def update(self):
        return

    async def delete(self, entity: T):
        orm = self._to_orm(entity)
        return await self.db.delete(orm)
