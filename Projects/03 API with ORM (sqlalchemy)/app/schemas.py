"""
This module contains the "Pydantic" models.
These Pydantic models define more or less a "schema" (a valid data shape).
"""

from pydantic import BaseModel, ConfigDict, EmailStr


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


# --------------------------------------


class UserBase(BaseModel):
    """Base Pydantic schema for users."""

    email: EmailStr


class UserCreate(UserBase):
    """Pydantic schema for creating users."""

    password: str


class UserUpdate(BaseModel):
    """Pydantic schema for updating users."""

    email: EmailStr | None = None
    is_active: bool | None = None


class User(UserBase):
    """Pydantic schema for reading users (response of API)."""

    id: int
    is_active: bool
    items: list[Item] = []

    model_config = ConfigDict(from_attributes=True)


class UserResetPassword(BaseModel):
    old_password: str
    new_password: str
    new_password_again: str


# ------------------------------------
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int


class Vote(BaseModel):
    item_id: int
    vote_dir: bool
