from config import settings
from db.models.user import RoleEnum
from db.models.user import User as DBUser
from fastapi import HTTPException, status
from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadData
from loguru import logger

serializer = URLSafeTimedSerializer(settings.secret_key)


def create_url_safe_token(data: dict, salt: str) -> str:
    return serializer.dumps(data, salt=salt)


def decode_url_safe_token(token: str, salt: str) -> dict | None:
    try:
        return serializer.loads(token, max_age=settings.token_expire, salt=salt)
    except BadData as e:
        logger.error(e)


def is_admin_or_current_user(user_id: int, current_user: DBUser):
    if current_user.is_admin:
        return
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowd to do this action.",
        )


def is_teacher(user: DBUser):
    if user.role != RoleEnum.TEACHER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only teachers can create a course.",
        )
