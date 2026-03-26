from sqlalchemy.ext.asyncio import AsyncSession


class RequestContext:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db
