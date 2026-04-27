from abc import abstractmethod

from typing import TypeVar, Generic
from uuid import UUID
from src.core.pagination import Pagination

from src.db.repositories.base_repository import BaseRepository
from src.core.exception import NotFoundError

T = TypeVar("T")  # Domain Object Dataclass
C = TypeVar("C")  # Create Schemas For Pydantic
U = TypeVar("U")  # Update Schema for Pydantic
M = TypeVar("M")  # Orm Model Type


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

    async def list(self, pagination: Pagination, filters=None) -> list[T]:
        return await self.repo.list(pagination, filters)

    async def create(self, data: C) -> T:
        entity: T = self._to_entity(data)
        return await self.repo.save(entity)

    async def update(self, entity_id: UUID, data: U) -> T:
        entity: T = await self.get_by_id(entity_id)
        updated_entity: T = await self._apply_update(entity, data)
        return await self.repo.save(updated_entity)

    async def delete(self, entity_id: UUID):
        return await self.repo.delete(entity_id)

    @abstractmethod
    def _to_entity(self, data: C) -> T:
        raise NotImplementedError()

    async def _apply_update(self, entity: T, data: U) -> T:
        raise NotImplementedError()
