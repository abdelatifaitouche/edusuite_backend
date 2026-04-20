from fastapi import APIRouter
from src.features.crm.router import router as company_router
from src.features.auth.routes import router as auth_router


api_router = APIRouter(prefix="/api/v1")


# api_router.include_router(company_router)
api_router.include_router(auth_router)
