from src.db.base import Base
from collections.abc import Sequence
from typing import TypeVar, Type, Generic
from src.core.pagination import Pagination
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from uuid import UUID
from src.core.request_context import RequestContext
from src.core.exception import NotFoundError
from abc import ABC

T = TypeVar("T")
M = TypeVar("M")


class BaseRepository(ABC, Generic[T, M]):
    model: type[M]

    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    def _apply_pagination(self, stmt, pagination: Pagination):
        return stmt.offset(pagination.offset).limit(pagination.page_size)

    def _apply_filters(self, stmt, filters):
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

    def _load_options(self):
        return []

    async def list(self, pagination: Pagination, filters=None) -> list[T]:
        stmt = select(self.model)

        # apply filters
        stmt = self._apply_filters(stmt, filters)
        # apply pagination
        stmt = self._apply_pagination(stmt, pagination)
        stmt = stmt.options(*self._load_options())
        results = await self.db.execute(stmt)
        data: list[M] = results.scalars().all()
        return [self._to_domain(row) for row in data]

    async def save(self, data: T) -> T:

        if getattr(data, "id", None) is None:
            orm = self._to_orm(data)
            self.db.add(orm)
        else:
            stmt = (
                select(self.model)
                .where(self.model.id == data.id)
                .options(*self._load_options())
            )

            result = await self.db.execute(stmt)

            orm = result.scalar_one_or_none()

            if not orm:
                raise NotFoundError(
                    message=f"{self.model.__name__} with ID {data.id} is not found"
                )
            orm = await self._orm_update(orm, data)

        await self.db.flush()
        await self.db.refresh(orm)
        return self._to_domain(orm)

    async def get_by_id(self, entity_id: UUID) -> T | None:

        stmt = (
            select(self.model)
            .where(self.model.id == entity_id)
            .options(*self._load_options())
        )

        result = await self.db.execute(stmt)

        orm = result.scalar_one_or_none()

        return self._to_domain(orm) if orm else None

    async def _orm_update(self, orm: M, entity: T) -> M:
        raise NotImplementedError()

    async def delete(self, entity_id: UUID):

        stmt = delete(self.model).where(self.model.id == entity_id)

        result = await self.db.execute(stmt)
        await self.db.flush()

        if result.rowcount <= 0:
            raise NotFoundError(
                message=f"{self.model.__name__} with id {entity_id} not found"
            )

        return result.rowcount > 0
