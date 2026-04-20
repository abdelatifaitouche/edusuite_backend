from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.core.config import settings


engine = create_async_engine(url=settings.DATABASE_URL, echo=True)

SessionLocal = async_sessionmaker(
    bind=engine, expire_on_commit=False, autoflush=False, autocommit=False
)


async def get_db():
    """
    Dependecy function to create a new async Session,
    uses a contextmanager to handle the session closing automaticaly on_exit

    rollsback on exceptions

    """

    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
