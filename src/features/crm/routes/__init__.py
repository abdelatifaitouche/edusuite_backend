from fastapi import APIRouter
from src.features.crm.routes.company_routes import router as company_router
from src.features.crm.routes.opportunity_routes import router as opportunity_router


router = APIRouter(prefix="/crm")

router.include_router(company_router)
router.include_router(opportunity_router)
