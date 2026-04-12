from sqlalchemy.ext.asyncio import AsyncSession


from src.features.auth.schemas.user import CreateUser, LoginUser, BaseUser
from src.features.auth.security.password import PasswordManager
from src.features.auth.repository.auth_repository import AuthRepository
from src.features.auth.models.users import UserModel
from src.features.auth.exceptions import WrongCredentialsError, UserAlreadyExistsError
from src.core.request_context import RequestContext
from src.features.auth.security.jwt import JwtManager
from src.features.auth.schemas.jwt_payload import JwtPayload


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db
        self.pwd_manager: PasswordManager = PasswordManager()
        self.repo: AuthRepository = AuthRepository(self.db)
        self.jwt_manager: JwtManager = JwtManager()

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

    async def login_user(self, data: LoginUser) -> str:
        user: UserModel | None = await self.repo.get_by_email(data.email)

        if user is None:
            raise WrongCredentialsError()

        if not self.pwd_manager.verify_password(data.password, user.password):
            raise WrongCredentialsError()

        access_token: str = self.jwt_manager.generate_token(
            JwtPayload(id=user.id, email=user.email, role=user.role),
        )

        return access_token
