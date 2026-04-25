from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.teams import service
from app.core.teams.exceptions import (
    DuplicateTeamNameError,
    MemberAlreadyInTeamError,
    MemberNotFoundError,
    MemberNotInTeamError,
    TeamNotFoundError,
)
from app.core.teams.schemas import TeamCreate, TeamUpdate
from app.db.session import get_session

router = APIRouter(prefix="/teams", tags=["teams"])


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_team(body: TeamCreate, session: AsyncSession = Depends(get_session)) -> dict:
    try:
        team = await service.create_team(session, body)
    except DuplicateTeamNameError as exc:
        raise HTTPException(status_code=409, detail=f"Team name already exists: {exc}") from exc
    return {"data": team.model_dump(), "error": None}


@router.get("", response_model=dict)
async def list_teams(session: AsyncSession = Depends(get_session)) -> dict:
    teams = await service.list_teams(session)
    return {"data": [t.model_dump() for t in teams], "error": None}


@router.get("/{team_id}", response_model=dict)
async def get_team(team_id: str, session: AsyncSession = Depends(get_session)) -> dict:
    team = await service.get_team(session, team_id)
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return {"data": team.model_dump(), "error": None}


@router.patch("/{team_id}", response_model=dict)
async def update_team(
    team_id: str, body: TeamUpdate, session: AsyncSession = Depends(get_session)
) -> dict:
    try:
        team = await service.update_team(session, team_id, body)
    except TeamNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Team not found") from exc
    except DuplicateTeamNameError as exc:
        raise HTTPException(status_code=409, detail=f"Team name already exists: {exc}") from exc
    return {"data": team.model_dump(), "error": None}


@router.delete("/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def archive_team(team_id: str, session: AsyncSession = Depends(get_session)) -> None:
    try:
        await service.archive_team(session, team_id)
    except TeamNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Team not found") from exc


@router.post("/{team_id}/members/{member_id}", response_model=dict)
async def assign_member(
    team_id: str, member_id: str, session: AsyncSession = Depends(get_session)
) -> dict:
    try:
        member = await service.assign_member(session, team_id, member_id)
    except TeamNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Team not found") from exc
    except MemberNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Member not found") from exc
    except MemberAlreadyInTeamError as exc:
        raise HTTPException(status_code=409, detail="Member already in team") from exc
    return {"data": member.model_dump(), "error": None}


@router.delete("/{team_id}/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    team_id: str, member_id: str, session: AsyncSession = Depends(get_session)
) -> None:
    try:
        await service.remove_member(session, team_id, member_id)
    except TeamNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Team not found") from exc
    except MemberNotInTeamError as exc:
        raise HTTPException(status_code=404, detail="Member not in team") from exc


@router.get("/{team_id}/members", response_model=dict)
async def list_team_members(team_id: str, session: AsyncSession = Depends(get_session)) -> dict:
    try:
        members = await service.list_team_members(session, team_id)
    except TeamNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Team not found") from exc
    return {"data": [m.model_dump() for m in members], "error": None}
