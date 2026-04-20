from sqlalchemy.ext.asyncio import AsyncSession
from src.features.training.repositories.formateur_repo import FormateurRepo


class FormateurUC:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db
        self.repo: FormateurRepo = FormateurRepo(self.db)
