from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.members import service
from app.core.members.exceptions import DuplicateSkillError
from app.core.members.schemas import SkillCreate
from app.db.session import get_session

router = APIRouter(prefix="/skills", tags=["skills"])


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_skill(body: SkillCreate, session: AsyncSession = Depends(get_session)) -> dict:
    try:
        skill = await service.create_skill(session, body)
    except DuplicateSkillError as exc:
        raise HTTPException(status_code=409, detail=f"Skill already exists: {exc}") from exc
    return {"data": skill.model_dump(), "error": None}


@router.get("", response_model=dict)
async def list_skills(session: AsyncSession = Depends(get_session)) -> dict:
    skills = await service.list_skills(session)
    return {"data": [s.model_dump() for s in skills], "error": None}
