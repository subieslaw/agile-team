from fastapi import APIRouter

from app.api.v1.endpoints.members import router as members_router
from app.api.v1.endpoints.skills import router as skills_router

router = APIRouter(prefix="/api/v1")
router.include_router(members_router)
router.include_router(skills_router)
