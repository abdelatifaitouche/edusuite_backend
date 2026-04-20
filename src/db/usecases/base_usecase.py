from typing import TypeVar, Generic
from uuid import UUID
from src.core.pagination import Pagination

from src.db.repositories.base_repository import BaseRepository
from src.core.exception import NotFoundError

T = TypeVar("T")  # Domain Object Dataclass
C = TypeVar("C")  # Create Schemas For Pydantic
U = TypeVar("U")
M = TypeVar("M")
from abc import ABC


class BaseUC(Generic[T, C, U]):
    def __init__(self, repo: "BaseRepository[T , M]"):
        self.repo = repo

    async def get_by_id(self, entity_id: UUID) -> T:
        result: T | None = await self.repo.get_by_id(entity_id)

        if not result:
            raise NotFoundError(
                message=f"{T.__class__.__name__} With ID {entity_id} was not Found"
            )

        return result

    async def list(self, pagination: Pagination) -> list[T]:
        return await self.repo.list(pagination)

    async def create(self, data: C) -> T:
        entity: T = self._to_entity(data)
        return await self.repo.save(entity)

    def _to_entity(self, data: C) -> T:
        raise NotImplementedError()

    async def _apply_update(self, entity: T, data: U) -> T:
        raise NotImplementedError()
