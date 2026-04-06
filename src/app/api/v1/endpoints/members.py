from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.members import service
from app.core.members.exceptions import DuplicateEmailError, SkillAlreadyAssignedError
from app.core.members.schemas import (
    MemberSkillCreate,
    TeamMemberCreate,
)
from app.db.session import get_session

router = APIRouter(prefix="/members", tags=["members"])


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_member(
    body: TeamMemberCreate, session: AsyncSession = Depends(get_session)
) -> dict:
    try:
        member = await service.create_member(session, body)
    except DuplicateEmailError as exc:
        raise HTTPException(status_code=409, detail=f"Email already registered: {exc}") from exc
    return {"data": member.model_dump(), "error": None}


@router.get("", response_model=dict)
async def list_members(session: AsyncSession = Depends(get_session)) -> dict:
    members = await service.list_members(session)
    return {"data": [m.model_dump() for m in members], "error": None}


@router.get("/{member_id}", response_model=dict)
async def get_member(member_id: str, session: AsyncSession = Depends(get_session)) -> dict:
    member = await service.get_member(session, member_id)
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"data": member.model_dump(), "error": None}


@router.post("/{member_id}/skills", response_model=dict, status_code=status.HTTP_201_CREATED)
async def assign_skill(
    member_id: str, body: MemberSkillCreate, session: AsyncSession = Depends(get_session)
) -> dict:
    try:
        result = await service.assign_skill(session, member_id, body)
    except SkillAlreadyAssignedError as exc:
        raise HTTPException(status_code=409, detail="Skill already assigned to member") from exc
    if result is None:
        raise HTTPException(status_code=404, detail="Member or skill not found")
    return {"data": result.model_dump(), "error": None}


@router.get("/{member_id}/skills", response_model=dict)
async def list_member_skills(member_id: str, session: AsyncSession = Depends(get_session)) -> dict:
    skills = await service.list_member_skills(session, member_id)
    if skills is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"data": [s.model_dump() for s in skills], "error": None}
