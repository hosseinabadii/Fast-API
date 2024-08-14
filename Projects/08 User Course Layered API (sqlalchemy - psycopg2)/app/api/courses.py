from crud.courses import (
    create_course,
    delete_course,
    get_course,
    get_courses,
    update_course,
)
from db.db_setup import SessionDep
from fastapi import APIRouter
from schemas.courses import Course, CourseCreate, CourseUpdate
from schemas.sections import Section

router = APIRouter(prefix="/api/courses", tags=["Courses"])


@router.post("/", response_model=Course, status_code=201)
async def api_create_course(course: CourseCreate, session: SessionDep):
    return create_course(session, course)


@router.get("/", response_model=list[Course])
async def api_get_courses(session: SessionDep):
    return get_courses(session)


@router.get("/{course_id}", response_model=Course)
async def api_get_course(course_id: int, session: SessionDep):
    return get_course(session, course_id)


@router.put("/{course_id}", response_model=Course, status_code=202)
async def api_update_course(course_id: int, course: CourseUpdate, session: SessionDep):
    return update_course(session, course_id, course)


@router.delete("/{course_id}", status_code=204)
async def api_delete_course(course_id: int, session: SessionDep):
    return delete_course(session, course_id)


@router.get("/{course_id}/sections", response_model=list[Section])
async def api_get_course_sections(course_id: int, session: SessionDep):
    db_course = get_course(session, course_id)
    return db_course.sections
