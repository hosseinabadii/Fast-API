from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.db.models.user import RoleEnum


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    role: RoleEnum
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    role: RoleEnum | None = None
    is_active: bool | None = None
    is_admin: bool | None = None


class UserResetPassword(BaseModel):
    old_password: str
    new_password: str
    new_password_again: str
