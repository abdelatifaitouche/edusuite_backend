from abc import ABC, abstractmethod


class IRepo(ABC):
    async def save(self):
        pass

    async def list(self):
        pass

    async def get_by_id(self):
        pass

    async def delete(self):
        pass

    async def update(self):
        pass
