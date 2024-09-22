from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CourseBase(BaseModel):
    title: str
    description: str | None = None


class CourseCreate(CourseBase): ...


class Course(CourseBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CourseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
