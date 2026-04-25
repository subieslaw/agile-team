from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.members.schemas import TeamMemberRead as TeamMemberRead  # re-export


class TeamCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None


class TeamUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    status: str | None = None


class TeamRead(BaseModel):
    id: str
    name: str
    description: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
