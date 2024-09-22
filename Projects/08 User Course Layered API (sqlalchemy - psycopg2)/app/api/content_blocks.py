from crud.content_blocks import (
    create_content_block,
    delete_content_block,
    get_content_block,
    get_content_blocks,
    update_content_block,
)
from db.db_setup import SessionDep
from fastapi import APIRouter
from schemas.content_blocks import (
    ContentBlock,
    ContentBlockCreate,
    ContentBlockUpdate,
)

router = APIRouter(prefix="/content-blocks", tags=["Content Blocks"])


@router.post("/", response_model=ContentBlock, status_code=201)
def api_create_content_block(content_block: ContentBlockCreate, session: SessionDep):
    return create_content_block(session, content_block)


@router.get("/", response_model=list[ContentBlock])
def api_get_content_blocks(session: SessionDep):
    return get_content_blocks(session)


@router.get("/{content_block_id}", response_model=ContentBlock)
def api_get_content_block(content_block_id: int, session: SessionDep):
    return get_content_block(session, content_block_id)


@router.put("/{content_block_id}", response_model=ContentBlock, status_code=202)
def api_update_content_block(
    content_block_id: int, content_block: ContentBlockUpdate, session: SessionDep
):
    return update_content_block(session, content_block_id, content_block)


@router.delete("/{content_block_id}", status_code=204)
def api_content_block_id(content_block_id: int, session: SessionDep):
    return delete_content_block(session, content_block_id)
