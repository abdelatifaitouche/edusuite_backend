from sqlalchemy.ext.asyncio import AsyncSession


from src.features.auth.schemas.user import CreateUser, LoginUser, BaseUser
from src.features.auth.security.password import PasswordManager
from src.features.auth.repository.auth_repository import AuthRepository
from src.features.auth.models.users import UserModel
from src.features.auth.exceptions import UserAlreadyExistsError
from src.core.request_context import RequestContext


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db
        self.pwd_manager: PasswordManager = PasswordManager()
        self.repo: AuthRepository = AuthRepository(self.db)

    async def list_users(self, ctx: RequestContext):
        users: list[UserModel] = await self.repo.list(ctx.pagination)
        return [BaseUser.model_validate(user) for user in users]

    async def create_user(self, data: CreateUser) -> BaseUser:
        user: UserModel | None = await self.repo.get_by_email(data.email)

        if user:
            raise UserAlreadyExistsError(data.email)

        hashed_password: str = self.pwd_manager.hash_password(data.password)

        user_model: UserModel = UserModel(
            email=data.email, password=hashed_password, role=data.role
        )

        await self.repo.save(user_model)

        await self.db.commit()

        return BaseUser.model_validate(user_model)

    async def login_user(self):
        return
