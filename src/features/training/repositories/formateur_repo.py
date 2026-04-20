from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories.base_repository import BaseRepository
from src.features.training.models.formateur import Formateur as FormateurDB


class FormateurRepo(BaseRepository[FormateurDB]):
    def __init__(self):
        super().__init__(FormateurDB)

    def block_formateur(self):
        return False
