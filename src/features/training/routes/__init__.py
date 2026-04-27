from fastapi import APIRouter
from src.features.training.routes.formateur_routes import router as formateur_routes
from src.features.training.routes.formation_routes import router as formation_routes


router = APIRouter(prefix="/training")

router.include_router(formateur_routes)
router.include_router(formation_routes)
