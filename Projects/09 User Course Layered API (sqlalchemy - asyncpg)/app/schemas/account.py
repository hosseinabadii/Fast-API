from pydantic import BaseModel, EmailStr


class EmailSchema(BaseModel):
    subject: str
    recipients: list[EmailStr]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenRefresh(BaseModel):
    token: str


class TokenData(BaseModel):
    jti: str
    email: EmailStr
    version: int

