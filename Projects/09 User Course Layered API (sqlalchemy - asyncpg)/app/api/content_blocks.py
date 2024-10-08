from fastapi import APIRouter

from app.crud.content_blocks import (
    create_content_block,
    delete_content_block,
    get_content_block,
    get_content_blocks,
    update_content_block,
)
from app.db.db_setup import SessionDep
from app.schemas.content_blocks import (
    ContentBlock,
    ContentBlockCreate,
    ContentBlockUpdate,
)

router = APIRouter(prefix="/content-blocks", tags=["Content Blocks"])


@router.post("/", response_model=ContentBlock, status_code=201)
async def api_create_content_block(
    content_block: ContentBlockCreate, session: SessionDep
):
    return await create_content_block(session, content_block)


@router.get("/", response_model=list[ContentBlock])
async def api_get_content_blocks(session: SessionDep):
    return await get_content_blocks(session)


@router.get("/{content_block_id}", response_model=ContentBlock)
async def api_get_content_block(content_block_id: int, session: SessionDep):
    return await get_content_block(session, content_block_id)


@router.put("/{content_block_id}", response_model=ContentBlock, status_code=202)
async def api_update_content_block(
    content_block_id: int, content_block: ContentBlockUpdate, session: SessionDep
):
    return await update_content_block(session, content_block_id, content_block)


@router.delete("/{content_block_id}", status_code=204)
async def api_content_block_id(content_block_id: int, session: SessionDep):
    return await delete_content_block(session, content_block_id)
