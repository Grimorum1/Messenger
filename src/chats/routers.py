from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocket, WebSocketDisconnect

from .schemas import ChatCreate
from . import service
from db.db_setup import db_helper
from messages.service import create_message

router = APIRouter(prefix='/chat', tags=['Chat',])


@router.websocket("/ws/{client_id}/{chat_id}")
async def websocket_endpoint(
        websocket: WebSocket,
        client_id: int,
        chat_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    await service.manager.connect(websocket, client_id, chat_id, session)
    try:
        while True:
            message = await websocket.receive_text()
            await create_message(message, client_id, chat_id, session)
            await service.manager.broadcast(message, client_id, chat_id, session)
    except WebSocketDisconnect:
        service.manager.disconnect(client_id, chat_id)


@router.post("/")
async def create_chat(
        chat: ChatCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> dict:
    chat_id = await service.create_chat(chat, session)
    return {"error": 0, "chat_id": chat_id}


@router.get("/")
async def get_chat(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> dict:
    chat_data = await service.get_chat(session)
    return {"data": chat_data}


@router.get("/{chat_id}")
async def get_chat(
        chat_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> dict:
    chat_data = await service.get_chat(session, chat_id)
    return {"data": chat_data}