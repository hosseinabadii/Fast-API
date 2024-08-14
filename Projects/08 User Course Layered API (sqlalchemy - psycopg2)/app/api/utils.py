from fastapi import HTTPException, status
from schemas.users import User


def is_current_user(user_id: int, current_user: User):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowd to do this action",
        )
