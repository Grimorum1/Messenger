from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_setup import db_helper
from groups.schemas import GroupCreate, GroupAddUser
from groups.service import create, join, get

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.post("/")
async def create_group(
        group: GroupCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> dict:
    data = await create(group, session)
    return {"error": 0, "data": data}


@router.post("/add_user/")
async def join_user(
        group_schema: GroupAddUser,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    res = await join(group_schema, session=session)
    return {"error": 0, "message": res}


@router.get("/")
async def get_groups(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    return await get(session)