from fastapi import APIRouter
from src.features.training.routes.formateur_routes import router as formateur_routes
from src.features.training.routes.formation_routes import router as formation_routes
from src.features.training.routes.objectif_routes import router as objectif_router
from src.features.training.routes.salle_routes import router as salle_router
from src.features.training.routes.session_routes import router as session_router


router = APIRouter(prefix="/training")

router.include_router(formateur_routes)
router.include_router(formation_routes)
router.include_router(objectif_router)
router.include_router(salle_router)
router.include_router(session_router)
