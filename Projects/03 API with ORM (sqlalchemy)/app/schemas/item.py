from pydantic import BaseModel, ConfigDict


class ItemBase(BaseModel):
    """Base Pydantic schema for items."""

    title: str
    description: str | None = None
    is_public: bool | None = None


class ItemCreate(ItemBase):
    """Pydantic schema for creating items."""


class ItemUpdate(BaseModel):
    """Pydantic schema for creating items."""

    title: str | None = None
    description: str | None = None
    is_public: bool | None = None


class Item(ItemBase):
    """Pydantic schema for reading items (response of API)."""

    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class ItemWithVoteCount(BaseModel):
    id: int
    title: str
    description: str | None
    is_public: bool | None
    owner_id: int
    vote_count: int

    model_config = ConfigDict(from_attributes=True)
