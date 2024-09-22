from pydantic import BaseModel, EmailStr


class EmailSchema(BaseModel):
    subject: str
    recipients: list[EmailStr]


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class TokenRefresh(BaseModel):
    token: str


class TokenData(BaseModel):
    email: EmailStr
