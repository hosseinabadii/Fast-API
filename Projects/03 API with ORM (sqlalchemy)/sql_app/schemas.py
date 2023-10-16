"""
This module contains the "Pydantic" models.
These Pydantic models define more or less a "schema" (a valid data shape).
"""

from pydantic import BaseModel, EmailStr
# from pydantic.types import conint


class ItemBase(BaseModel):
    """Base Pydantic schema for items."""
    title: str
    description: str | None = None
    is_public: bool | None = None


class ItemCreate(ItemBase):
    """Pydantic schema for creating items."""


class Item(ItemBase):
    """Pydantic schema for reading items (response of API)."""
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class ItemVote(BaseModel):
    Item: Item
    votes: str

    class Config:
        orm_mode = True

# --------------------------------------

class UserBase(BaseModel):
    """Base Pydantic schema for users."""
    email: EmailStr


class UserCreate(UserBase):
    """Pydantic schema for creating users."""
    password: str


class UserUpdate(UserBase):
    """Pydantic schema for updating users."""
    is_active: bool


class User(UserBase):
    """Pydantic schema for reading users (response of API)."""
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True


class UserResetPassword(BaseModel):
    old_password: str
    new_password: str
    new_password_again: str


# ------------------------------------
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str | None = None


class Vote(BaseModel):
    item_id: int
    vote_dir: bool
