import logging

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from config import settings
from db.db_setup import db_helper
from .model import Message
from .schemas import MessageRead
from .service import delete_messages_by_chat_id as delete_service

router = APIRouter(prefix='/messages', tags=['Messages'])


logger = logging.getLogger(__name__)
logging.basicConfig(level=settings.level_logger)

@router.delete('/by_chat_id/{chat_id}')
async def delete_messages_by_chat_id(
    chat_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    """
    Удаляет все сообщения из указанного чата.
    """
    try:
        await delete_service(chat_id, session)
        logger.info(f"Удалены сообщения из чата с ID {chat_id}")
        return {"detail": f"Сообщения из чата {chat_id} удалены."}
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при удалении сообщений из чата {chat_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при удалении сообщений из чата."
        )


@router.get("/history/{chat_id}", response_model=list[MessageRead])
async def get_message_history(
    chat_id: int,
    limit: int = Query(50, ge=1),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """
    Возвращает историю сообщений чата с постраничной навигацией.
    """
    try:
        stmt = (
            select(Message)
            .where(Message.chat_id == chat_id)
            .order_by(Message.timestamp.asc())
            .offset(offset)
            .limit(limit)
        )
        result = await session.execute(stmt)
        messages = result.scalars().all()
        logger.info(f"Получена история сообщений чата {chat_id} (limit={limit}, offset={offset})")
        return messages
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении истории сообщений чата {chat_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при получении истории сообщений чата."
        )
