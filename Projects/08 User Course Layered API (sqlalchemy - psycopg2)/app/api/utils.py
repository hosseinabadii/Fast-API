from db.models.user import RoleEnum
from fastapi import HTTPException, status
from db.models.user import User as DBUser


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
