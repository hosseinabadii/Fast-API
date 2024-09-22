from crud.users import (
    update_user,
)
from db.db_setup import SessionDep
from dependency import CurrentAdminUserDep
from fastapi import APIRouter
from schemas.users import User, UserUpdate

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.put(
    "/update-user/{user_id}",
    response_model=User,
    status_code=202,
    dependencies=[CurrentAdminUserDep],
)
async def api_update_user(
    user_id: int,
    user: UserUpdate,
    session: SessionDep,
):
    return await update_user(session, user_id, user)
