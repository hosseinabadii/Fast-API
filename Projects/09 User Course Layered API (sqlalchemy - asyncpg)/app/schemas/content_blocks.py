from datetime import datetime

from pydantic import BaseModel, ConfigDict, HttpUrl

from app.db.models.course import ContentType


class ContentBlockBase(BaseModel):
    title: str
    description: str | None = None
    type: ContentType
    content: str | None = None
    url: HttpUrl | None = None
    section_id: int


class ContentBlockCreate(ContentBlockBase): ...


class ContentBlock(ContentBlockBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ContentBlockUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    type: ContentType | None = None
    content: str | None = None
    url: HttpUrl | None = None
