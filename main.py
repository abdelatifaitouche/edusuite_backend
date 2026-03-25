from fastapi import FastAPI
from src.api.router import api_router
from src.db.session import engine
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(title="EduSuite API", version="1.0.0", lifespan=lifespan)


app.include_router(api_router)


@app.get("/health")
def health():
    return {"status": "ok"}
