from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from crud.users import get_user_by_email
from db.db_setup import SessionDep
from db.models.user import User as DBUser
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from schemas.users import User
from sqlalchemy.orm import Session

from .auth_schemas import TokenData
from .utils import verify_password

CREDENTIAL_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def authenticate_user(session: Session, email: str, password: str) -> DBUser | None:
    db_user = get_user_by_email(session, email)
    if not db_user:
        return
    if not verify_password(password, db_user.password):
        return
    return db_user


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt


def verify_access_token(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
    try:
        payload: dict[str, str] = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        user_email = payload.get("user_email")
        if user_email is None:
            raise CREDENTIAL_EXCEPTION
        token_data = TokenData(email=user_email)
    except jwt.ExpiredSignatureError as exc:
        raise CREDENTIAL_EXCEPTION from exc
    return token_data


AccessTokenDep = Annotated[TokenData, Depends(verify_access_token)]


def get_current_user(token_data: AccessTokenDep, session: SessionDep) -> DBUser:
    current_user = get_user_by_email(session, token_data.email)
    if not current_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return current_user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
