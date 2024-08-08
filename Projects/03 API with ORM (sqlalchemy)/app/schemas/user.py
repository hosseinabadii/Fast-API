from pydantic import BaseModel, ConfigDict, EmailStr

from .item import Item


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
