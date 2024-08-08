from pydantic import EmailStr
from sqlmodel import AutoString, Field, Relationship, SQLModel


# ----------------------------------
#    User Models
# ----------------------------------
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, sa_type=AutoString)
    name: str | None = Field(default=None, min_length=4, max_length=20)
    age: int | None = Field(default=None, gt=0, le=150)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    is_active: bool = True
    items: list["Item"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    pass


class UserUpdate(UserBase):
    email: str | None = None
    password: str | None = None
    is_active: bool | None = None


class UserPublicWithItems(UserBase):
    items: list["ItemPublic"] = []


class UserResetPassword(SQLModel):
    old_password: str
    new_password: str
    confirm_password: str


class ForgotPasswordRequest(SQLModel):
    email: EmailStr = Field(sa_type=AutoString)


class ForgotPasswordReset(SQLModel):
    token: str
    new_password: str
    confirm_password: str


# ----------------------------------
#    Item Models
# ----------------------------------
class ItemBase(SQLModel):
    title: str
    description: str | None = None
    is_public: bool = False


class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    user: User | None = Relationship(back_populates="items")


class ItemCreate(ItemBase):
    pass


class ItemPublic(ItemBase):
    id: int
    user_id: int


class ItemUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    is_public: bool | None = None


class ItemPublicForUser(ItemBase):
    id: int


# # # ----------------------------------
# # #    Token Models
# # # ----------------------------------
class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    id: int | None = None
