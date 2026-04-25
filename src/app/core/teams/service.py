from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.teams.exceptions import (
    DuplicateTeamNameError,
    MemberAlreadyInTeamError,
    MemberNotFoundError,
    MemberNotInTeamError,
    TeamNotFoundError,
)
from app.core.teams.schemas import TeamCreate, TeamMemberRead, TeamRead, TeamUpdate
from app.db.models import TeamMember
from app.db.models.team import Team


async def create_team(session: AsyncSession, data: TeamCreate) -> TeamRead:
    team = Team(name=data.name, description=data.description)
    session.add(team)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise DuplicateTeamNameError(data.name)
    await session.refresh(team)
    return TeamRead.model_validate(team)


async def list_teams(session: AsyncSession) -> list[TeamRead]:
    result = await session.execute(
        select(Team).where(Team.status != "archived").order_by(Team.name)
    )
    return [TeamRead.model_validate(t) for t in result.scalars()]


async def get_team(session: AsyncSession, team_id: str) -> TeamRead | None:
    team = await session.get(Team, team_id)
    if team is None or team.status == "archived":
        return None
    return TeamRead.model_validate(team)


async def update_team(session: AsyncSession, team_id: str, data: TeamUpdate) -> TeamRead:
    team = await session.get(Team, team_id)
    if team is None:
        raise TeamNotFoundError(team_id)
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(team, field, value)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise DuplicateTeamNameError(data.name)
    await session.refresh(team)
    return TeamRead.model_validate(team)


async def archive_team(session: AsyncSession, team_id: str) -> None:
    team = await session.get(Team, team_id)
    if team is None:
        raise TeamNotFoundError(team_id)
    team.status = "archived"
    await session.commit()


async def assign_member(session: AsyncSession, team_id: str, member_id: str) -> TeamMemberRead:
    team = await session.get(Team, team_id)
    if team is None:
        raise TeamNotFoundError(team_id)
    member = await session.get(TeamMember, member_id)
    if member is None:
        raise MemberNotFoundError(member_id)
    if member.team_id == team_id:
        raise MemberAlreadyInTeamError(member_id)
    member.team_id = team_id
    await session.commit()
    await session.refresh(member)
    return TeamMemberRead.model_validate(member)


async def remove_member(session: AsyncSession, team_id: str, member_id: str) -> None:
    team = await session.get(Team, team_id)
    if team is None:
        raise TeamNotFoundError(team_id)
    member = await session.get(TeamMember, member_id)
    if member is None or member.team_id != team_id:
        raise MemberNotInTeamError(member_id)
    member.team_id = None
    await session.commit()


async def list_team_members(session: AsyncSession, team_id: str) -> list[TeamMemberRead]:
    team = await session.get(Team, team_id)
    if team is None:
        raise TeamNotFoundError(team_id)
    result = await session.execute(
        select(TeamMember)
        .where(TeamMember.team_id == team_id)
        .where(TeamMember.is_active.is_(True))
    )
    return [TeamMemberRead.model_validate(m) for m in result.scalars()]
