from fastapi import APIRouter

from app.crud.sections import (
    create_section,
    delete_section,
    get_section,
    get_sections,
    update_section,
)
from app.db.db_setup import SessionDep
from app.schemas.content_blocks import ContentBlock
from app.schemas.sections import Section, SectionCreate, SectionUpdate

router = APIRouter(prefix="/sections", tags=["Sections"])


@router.post("/", response_model=Section, status_code=201)
async def api_create_section(section: SectionCreate, session: SessionDep):
    return await create_section(session, section)


@router.get("/", response_model=list[Section])
async def api_get_sections(session: SessionDep):
    return await get_sections(session)


@router.get("/{section_id}", response_model=Section)
async def api_get_section(section_id: int, session: SessionDep):
    return await get_section(session, section_id)


@router.put("/{section_id}", response_model=Section, status_code=202)
async def api_update_section(
    section_id: int, section: SectionUpdate, session: SessionDep
):
    return await update_section(session, section_id, section)


@router.delete("/{section_id}", status_code=204)
async def api_delete_section(section_id: int, session: SessionDep):
    return await delete_section(session, section_id)


@router.get("/{section_id}/content-blocks", response_model=list[ContentBlock])
async def api_get_section_content_blocks(section_id: int, session: SessionDep):
    db_section = await get_section(session, section_id)
    await session.refresh(db_section, attribute_names=["content_blocks"])
    return db_section.content_blocks
