from crud.content_blocks import (
    create_content_block,
    delete_content_block,
    get_content_block,
    get_content_blocks,
    update_content_block,
)
from fastapi import APIRouter
from schemas.content_blocks import (
    ContentBlock,
    ContentBlockCreate,
    ContentBlockUpdate,
)

from .dependencies.core import SessionDep

router = APIRouter(prefix="/api/content-blocks", tags=["Content Blocks"])


@router.post("/", response_model=ContentBlock, status_code=201)
async def api_create_content_block(
    content_block: ContentBlockCreate, session: SessionDep
):
    return create_content_block(session=session, content_block=content_block)


@router.get("/", response_model=list[ContentBlock])
async def api_get_content_blocks(session: SessionDep):
    return get_content_blocks(session=session)


@router.get("/{content_block_id}", response_model=ContentBlock)
async def api_get_content_block(content_block_id: int, session: SessionDep):
    return get_content_block(session=session, content_block_id=content_block_id)


@router.put("/{content_block_id}", response_model=ContentBlock, status_code=202)
async def api_update_content_block(
    content_block_id: int, content_block: ContentBlockUpdate, session: SessionDep
):
    return update_content_block(
        session=session, content_block_id=content_block_id, content_block=content_block
    )


@router.delete("/{content_block_id}", status_code=204)
async def api_content_block_id(content_block_id: int, session: SessionDep):
    return delete_content_block(session=session, content_block_id=content_block_id)


# @router.get("/{course_id}/sections", response_model=list[Section])
# async def api_get_course_sections(course_id: int, session: SessionDep):
#     db_course = get_course(session=session, course_id=course_id)
#     return db_course.sections
