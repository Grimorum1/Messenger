import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from db.db_setup import db_helper
from groups.schemas import GroupCreate, GroupAddUser
from groups.service import create, join, get

router = APIRouter(prefix="/groups", tags=["Groups"])

logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.level_logger)

@router.post("/")
async def create_group(
        group: GroupCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> dict:
    """
    Создаёт новую группу.
    """
    try:
        data = await create(group, session)
        logger.info(f"Создана группа '{group.name}' с ID {data.get('group_id')}")
        return {"error": 0, "data": data}
    except Exception as e:
        logger.error(f"Ошибка при создании группы '{group.name}': {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Ошибка при создании группы")


@router.post("/add_user/")
async def join_user(
        group_schema: GroupAddUser,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    """
    Добавляет пользователя в группу.
    """
    try:
        res = await join(group_schema, session=session)
        logger.info(f"Пользователь {group_schema.user_id} добавлен в группу {group_schema.group_id}")
        return {"error": 0, "message": res}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при добавлении пользователя {group_schema.user_id} в группу {group_schema.group_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Ошибка при добавлении пользователя в группу")


@router.get("/")
async def get_groups(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    """
    Возвращает список всех групп.
    """
    try:
        groups = await get(session)
        logger.info(f"Получен список групп, всего: {len(groups)}")
        return groups
    except Exception as e:
        logger.error(f"Ошибка при получении списка групп: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Ошибка при получении списка групп")
