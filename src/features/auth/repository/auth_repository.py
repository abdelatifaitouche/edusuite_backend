from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.repositories.base_repository import BaseRepository
from src.features.auth.models.users import UserModel


class AuthRepository(BaseRepository[UserModel]):
    def __init__(self, db: AsyncSession):
        self.db = db
        super().__init__(self.db, UserModel)

    async def get_by_email(self, email: str) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.db.execute(stmt)
        user: UserModel | None = result.scalar_one_or_none()
        return user
