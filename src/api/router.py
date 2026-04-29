from fastapi import APIRouter
from src.features.crm.routes import router as crm_router
from src.features.auth.routes import router as auth_router
from src.features.training.routes import router as training_router

api_router = APIRouter(prefix="/api/v1")


api_router.include_router(crm_router)
api_router.include_router(auth_router)
api_router.include_router(training_router)
