import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from chats.schemas import ChatCreate, ChatType
from chats.service import create_chat
from config import settings
from groups.model import Group
from groups.schemas import GroupCreate, GroupAddUser


logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.level_logger)

async def create(group_schema: GroupCreate, session: AsyncSession) -> dict:
    if not group_schema.members_list:
        group_schema.members_list = []
    if group_schema.creator_id not in group_schema.members_list:
        group_schema.members_list.append(group_schema.creator_id)
    group = Group(**group_schema.model_dump())
    session.add(group)
    await session.commit()
    chat_id = await create_chat(ChatCreate(name=group.name, type=ChatType.group), session)
    return {"chat_id": chat_id, "group_id": group.id}


async def join(group_schema: GroupAddUser, session: AsyncSession) -> str:
    result = await session.execute(select(Group).where(Group.id == group_schema.group_id))
    group = result.scalars().first()

    if not group:
        logger.warning(f"Попытка добавить пользователя в несуществующую группу с ID {group_schema.group_id}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Группа с ID {group_schema.group_id} не найдена")

    if group.members_list is None:
        group.members_list = []

    if group_schema.user_id in group.members_list:
        return "Пользователь уже в группе"

    group.members_list.append(group_schema.user_id)
    await session.commit()
    return "Пользователь добавлен в группу"


async def get(session: AsyncSession):
    result = await session.execute(select(Group))
    groups = result.scalars().all()
    return list(groups)
