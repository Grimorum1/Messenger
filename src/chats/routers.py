import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect

from .schemas import ChatCreate
from . import service
from db.db_setup import db_helper
from messages.service import create_message

router = APIRouter(prefix='/chat', tags=['Chat',])

logger = logging.getLogger("chat")
logging.basicConfig(level=logging.INFO)  # или DEBUG для подробного лога


@router.websocket("/ws/{client_id}/{chat_id}")
async def websocket_endpoint(
        websocket: WebSocket,
        client_id: int,
        chat_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    """
    WebSocket для обмена сообщениями в чате.
    """
    try:
        await service.manager.connect(websocket, client_id, chat_id, session)
        logger.info(f"Пользователь {client_id} подключился к чату {chat_id} через WebSocket.")
        while True:
            try:
                message = await websocket.receive_text()
                logger.debug(f"Получено сообщение от пользователя {client_id} в чате {chat_id}: {message}")
                await create_message(message, client_id, chat_id, session)
                await service.manager.broadcast(message, client_id, chat_id, session)
            except Exception as e:
                logger.error(f"Ошибка при обработке сообщения в чате {chat_id} от пользователя {client_id}: {e}")
                await websocket.close(code=1011)  # Внутренняя ошибка
                break
    except WebSocketDisconnect:
        service.manager.disconnect(client_id, chat_id)
        logger.info(f"Пользователь {client_id} отключился от чата {chat_id}.")
    except Exception as e:
        logger.error(f"Неожиданная ошибка WebSocket-соединения (пользователь {client_id}, чат {chat_id}): {e}")
        await websocket.close(code=1011)



@router.post("/")
async def create_chat(
        chat: ChatCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> dict:
    """
    Создаёт новый чат.
    """
    try:
        chat_id = await service.create_chat(chat, session)
        logger.info(f"Создали чат - {chat_id}.")
        return {"error": 0, "chat_id": chat_id}
    except Exception as e:
        logger.error(f"Ошибка при создании чата: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Ошибка при создании чата")


@router.get("/")
async def get_all_chats(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> dict:
    """
    Возвращает список всех чатов.
    """
    try:
        chat_data = await service.get_chat(session)
        return {"data": chat_data}
    except Exception as e:
        logger.error(f"Ошибка получения чатов: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Ошибка при получении списка чатов")


@router.get("/{chat_id}")
async def get_chat_by_id(
        chat_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> dict:
    """
    Возвращает данные конкретного чата.
    """
    try:
        chat_data = await service.get_chat(session, chat_id)
        if not chat_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Чат с id {chat_id} не найден")
        return {"data": chat_data}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка получения чата {chat_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Ошибка при получении данных чата")
