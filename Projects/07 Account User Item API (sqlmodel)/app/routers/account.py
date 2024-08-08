from pathlib import Path
from typing import Annotated

import oauth2
from config import settings
from db.db_setup import get_session
from db.models import (
    ForgotPasswordRequest,
    ForgotPasswordReset,
    Token,
    User,
    UserCreate,
    UserPublic,
    UserPublicWithItems,
    UserUpdate,
)
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from oauth2 import (
    create_reset_password_token,
    decode_reset_password_token,
    get_current_user,
)
from sqlmodel import Session, select
from utils import get_password_hash, send_fake_email, verify_password

templates_dir = Path(__file__).parent.parent / "templates"
templates = Jinja2Templates(directory=templates_dir)


router = APIRouter(prefix="/account", tags=["Account"])


@router.post("/signup", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def sign_up(
    user: UserCreate,
    session: Session = Depends(get_session),
) -> User:
    user_exists = session.exec(select(User).where(User.email == user.email)).first()
    if user_exists:
        raise HTTPException(
            status_code=400, detail=f"Email: {user.email} already registered."
        )
    hashed_password = get_password_hash(user.password)
    extra_data = {"hashed_password": hashed_password}
    db_user = User.model_validate(user, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.post("/login", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
):
    user = session.exec(select(User).where(User.email == form_data.username)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )
    verified = verify_password(form_data.password, user.hashed_password)
    if not verified:
        raise HTTPException(status_code=403, detail="Invalid Credentials")
    access_token = oauth2.create_access_token({"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/logout", response_class=HTMLResponse)
def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response


@router.get("/profile", response_model=UserPublicWithItems)
def read_profile(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.patch(
    "/update-profile",
    response_model=UserPublic,
    status_code=status.HTTP_202_ACCEPTED,
)
def update_profile(
    user: UserUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> User:
    user_data = user.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(user_data)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


@router.delete("/delete-profile", response_model=UserPublic)
def delete_profile(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> User:
    session.delete(current_user)
    session.commit()
    return current_user


@router.get("/forgot-password", response_class=HTMLResponse)
def forgot_password_form(request: Request):
    return templates.TemplateResponse("forgot_password_form.html", {"request": request})


@router.post("/forgot-password", status_code=status.HTTP_202_ACCEPTED)
def forgot_password(
    fp_request: ForgotPasswordRequest, session: Session = Depends(get_session)
) -> None:
    print(fp_request)
    user = session.exec(select(User).where(User.email == fp_request.email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    token = create_reset_password_token(email=user.email)

    reset_url_link = f"{settings.app_host}/{settings.reset_password_url}/?token={token}"
    send_fake_email(reset_url_link)


@router.get("/reset-password", response_class=HTMLResponse)
def reset_password_form(request: Request, token: str):
    return templates.TemplateResponse(
        "reset_password_form.html", {"request": request, "token": token}
    )


@router.post("/reset-password", status_code=status.HTTP_202_ACCEPTED)
def reset_password(
    fp_reset: ForgotPasswordReset, session: Session = Depends(get_session)
) -> None:
    print(fp_reset)
    email = decode_reset_password_token(fp_reset.token)
    print(f"{email=}")
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if fp_reset.new_password != fp_reset.confirm_password:
        raise HTTPException(status_code=403, detail="New passwords do not match.")

    user.hashed_password = get_password_hash(fp_reset.new_password)
    session.add(user)
    session.commit()
