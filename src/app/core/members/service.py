from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.members.exceptions import (
    DuplicateEmailError,
    DuplicateSkillError,
    SkillAlreadyAssignedError,
)
from app.core.members.schemas import (
    MemberSkillCreate,
    MemberSkillRead,
    SkillCreate,
    SkillRead,
    TeamMemberCreate,
    TeamMemberRead,
)
from app.db.models import MemberSkill, Skill, TeamMember


async def create_member(session: AsyncSession, data: TeamMemberCreate) -> TeamMemberRead:
    member = TeamMember(**data.model_dump())
    session.add(member)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise DuplicateEmailError(data.email)
    await session.refresh(member)
    return TeamMemberRead.model_validate(member)


async def list_members(session: AsyncSession) -> list[TeamMemberRead]:
    result = await session.execute(select(TeamMember).where(TeamMember.is_active.is_(True)))
    return [TeamMemberRead.model_validate(m) for m in result.scalars()]


async def get_member(session: AsyncSession, member_id: str) -> TeamMemberRead | None:
    member = await session.get(TeamMember, member_id)
    if member is None:
        return None
    return TeamMemberRead.model_validate(member)


async def create_skill(session: AsyncSession, data: SkillCreate) -> SkillRead:
    skill = Skill(**data.model_dump())
    session.add(skill)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise DuplicateSkillError(data.name)
    await session.refresh(skill)
    return SkillRead.model_validate(skill)


async def list_skills(session: AsyncSession) -> list[SkillRead]:
    result = await session.execute(select(Skill))
    return [SkillRead.model_validate(s) for s in result.scalars()]


async def assign_skill(
    session: AsyncSession, member_id: str, data: MemberSkillCreate
) -> MemberSkillRead | None:
    member = await session.get(TeamMember, member_id)
    if member is None:
        return None
    skill = await session.get(Skill, data.skill_id)
    if skill is None:
        return None
    ms = MemberSkill(
        member_id=member_id,
        skill_id=data.skill_id,
        proficiency=data.proficiency,
        years_exp=data.years_exp,
    )
    session.add(ms)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise SkillAlreadyAssignedError(data.skill_id)
    await session.refresh(ms)
    return MemberSkillRead(
        id=ms.id,
        skill_id=ms.skill_id,
        skill_name=skill.name,
        proficiency=ms.proficiency,
        years_exp=float(ms.years_exp) if ms.years_exp is not None else None,
    )


async def list_member_skills(session: AsyncSession, member_id: str) -> list[MemberSkillRead] | None:
    member = await session.get(TeamMember, member_id)
    if member is None:
        return None
    result = await session.execute(
        select(MemberSkill)
        .where(MemberSkill.member_id == member_id)
        .options(selectinload(MemberSkill.skill))
    )
    return [
        MemberSkillRead(
            id=ms.id,
            skill_id=ms.skill_id,
            skill_name=ms.skill.name,
            proficiency=ms.proficiency,
            years_exp=float(ms.years_exp) if ms.years_exp is not None else None,
        )
        for ms in result.scalars()
    ]
