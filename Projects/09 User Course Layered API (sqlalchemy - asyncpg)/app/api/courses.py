from fastapi import APIRouter

from app.crud.courses import (
    create_course,
    delete_course,
    get_course,
    get_courses,
    update_course,
)
from app.db.db_setup import SessionDep
from app.dependencies import CurrentUserDep
from app.schemas.courses import Course, CourseCreate, CourseUpdate
from app.schemas.sections import Section
from app.utils import is_admin_or_current_user, is_teacher

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.post("/", response_model=Course, status_code=201)
async def api_create_course(
    course: CourseCreate, current_user: CurrentUserDep, session: SessionDep
):
    is_teacher(current_user)
    return await create_course(session, course, current_user.id)


@router.get("/", response_model=list[Course])
async def api_get_courses(session: SessionDep):
    return await get_courses(session)


@router.get("/{course_id}", response_model=Course)
async def api_get_course(course_id: int, session: SessionDep):
    return await get_course(session, course_id)


@router.put("/{course_id}", response_model=Course, status_code=202)
async def api_update_course(
    course_id: int,
    course: CourseUpdate,
    current_user: CurrentUserDep,
    session: SessionDep,
):
    db_course = await get_course(session, course_id)
    is_admin_or_current_user(db_course.user_id, current_user)
    return await update_course(session, db_course, course)


@router.delete("/{course_id}", status_code=204)
async def api_delete_course(
    course_id: int, current_user: CurrentUserDep, session: SessionDep
):
    db_course = await get_course(session, course_id)
    is_admin_or_current_user(db_course.user_id, current_user)
    return await delete_course(session, db_course)


@router.get("/{course_id}/sections", response_model=list[Section])
async def api_get_course_sections(course_id: int, session: SessionDep):
    db_course = await get_course(session, course_id)
    await session.refresh(db_course, attribute_names=["sections"])
    return db_course.sections
