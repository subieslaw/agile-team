from pydantic import BaseModel, EmailStr, Field


class TeamMemberCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    role: str | None = Field(None, max_length=100)
    team: str | None = Field(None, max_length=100)


class TeamMemberRead(BaseModel):
    id: str
    name: str
    email: str
    role: str | None
    team: str | None
    is_active: bool

    model_config = {"from_attributes": True}


class SkillCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    category: str | None = Field(None, max_length=100)


class SkillRead(BaseModel):
    id: str
    name: str
    category: str | None

    model_config = {"from_attributes": True}


class MemberSkillCreate(BaseModel):
    skill_id: str
    proficiency: int | None = Field(None, ge=1, le=5)
    years_exp: float | None = Field(None, ge=0)


class MemberSkillRead(BaseModel):
    id: str
    skill_id: str
    skill_name: str
    proficiency: int | None
    years_exp: float | None

    model_config = {"from_attributes": True}
