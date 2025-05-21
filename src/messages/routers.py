from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_setup import db_helper
from .model import Message
from .schemas import MessageRead
from .service import delete_messages_by_chat_id as delete_service

router = APIRouter(prefix='/messages', tags=['Messages'])


@router.delete('/by_chat_id/{chat_id}')
async def delete_messages_by_chat_id(
    chat_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    await delete_service(chat_id, session)
    return {"detail": f"Messages from chat {chat_id} deleted."}



@router.get("/history/{chat_id}", response_model=list[MessageRead])
async def get_message_history(
    chat_id: int,
    limit: int = Query(50, ge=1),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    stmt = (
        select(Message)
        .where(Message.chat_id == chat_id)
        .order_by(Message.timestamp.asc())
        .offset(offset)
        .limit(limit)
    )
    result = await session.execute(stmt)
    messages = result.scalars().all()
    return messages