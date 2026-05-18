from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from src.api.router import api_router
from src.db.session import engine
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import src.db.models
from src.core.exception import AppException


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(title="EduSuite API", version="1.0.0", lifespan=lifespan)


@app.exception_handler(AppException)
async def app_exception_handler(request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(
            {
                "error": exc.__class__.__name__,
                "message": exc.message,
                "details": exc.details,
            }
        ),
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # your frontend URL
    allow_credentials=True,  # required for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)


@app.get("/health")
def health():
    return {"status": "ok"}
