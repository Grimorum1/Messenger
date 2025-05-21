import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from db.db_setup import db_helper as db_base
from . import service, schemas

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
async def add_user(
    user: schemas.UserCreate,
    session: AsyncSession = Depends(db_base.scoped_session_dependency),
):
    """
    Создаёт нового пользователя.
    """
    try:
        new_user = await service.create_users(user=user, session=session)
        logger.info(f"Создан пользователь с ID: {new_user.id}")
        return new_user
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при создании пользователя: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при создании пользователя."
        )


@router.get("/", response_model=list[schemas.UserBase])
async def get_users(
    session: AsyncSession = Depends(db_base.scoped_session_dependency),
):
    """
    Возвращает список всех пользователей.
    """
    try:
        users = await service.get_users(session=session)
        logger.info(f"Получен список пользователей, всего: {len(users)}")
        return users
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении списка пользователей: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при получении списка пользователей."
        )


@router.get("/{user_id}/", response_model=schemas.UserBase)
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(db_base.scoped_session_dependency),
):
    """
    Возвращает информацию о пользователе по ID.

    Возвращает 404, если пользователь не найден.
    """
    try:
        user = await service.get_user(session=session, user_id=user_id)
        if user:
            logger.info(f"Пользователь с ID {user_id} найден.")
            return user
        else:
            logger.warning(f"Пользователь с ID {user_id} не найден.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found!",
            )
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при поиске пользователя с ID {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при поиске пользователя."
        )
