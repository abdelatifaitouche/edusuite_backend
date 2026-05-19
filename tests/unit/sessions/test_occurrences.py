import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from src.features.training.repositories.occurrence_repo import OccurrenceRepository


load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("Couldnt load database url")

engine = create_engine(DATABASE_URL)
sessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    with sessionLocal() as session:
        try:
            yield session
        except Exception as e:
            raise e


@pytest.fixture
def repo():
    return OccurrenceRepository(db=sessionLocal())
