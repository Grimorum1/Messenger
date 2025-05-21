from sqlalchemy import update, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from messages.model import Message


async def create_message(
        message: str,
        client_id: int,
        chat_id: int,
        session: AsyncSession
):
    mes = Message(chat_id=chat_id, sender_id=client_id, text=message)
    session.add(mes)
    await session.commit()


async def message_is_read(
        sender_id: int,
        chat_id: int,
        session: AsyncSession,
        not_in_sender: bool = False
):
    condition = Message.sender_id != sender_id if not_in_sender else Message.sender_id == sender_id

    update_stmt = (
        update(Message)
        .where(
            and_(
                Message.chat_id == chat_id,
                condition
            )
        )
        .values(is_read=True)
    )
    await session.execute(update_stmt)
    await session.commit()


async def delete_messages_by_chat_id(chat_id: int, session: AsyncSession):
    stmt = delete(Message).where(Message.chat_id == chat_id)
    await session.execute(stmt)
    await session.commit()
