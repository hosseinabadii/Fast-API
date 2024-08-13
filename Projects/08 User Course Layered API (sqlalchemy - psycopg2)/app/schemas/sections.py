from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SectionBase(BaseModel):
    title: str
    description: str | None = None
    course_id: int


class SectionCreate(SectionBase): ...


class Section(SectionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SectionUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
