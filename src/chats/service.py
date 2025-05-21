from typing import Dict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from starlette.websockets import WebSocket

from chats.model import Chat, UserChatAssociation
from chats.schemas import ChatCreate
from messages.model import Message
from messages.service import message_is_read
from users.model import User


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, Dict[int, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int, room_id: int, session: AsyncSession):
        """
        Устанавливает соединение с пользователем.
        websocket.accept() — подтверждает подключение.
        """
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = {}
        self.active_connections[room_id][user_id] = websocket
        await message_is_read(user_id, room_id, session, not_in_sender=True)

    def disconnect(self, user_id: int, room_id: int):
        """
        Закрывает соединение и удаляет его из списка активных подключений.
        Если в комнате больше нет пользователей, удаляет комнату.
        """
        if room_id in self.active_connections and user_id in self.active_connections[room_id]:
            del self.active_connections[room_id][user_id]
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    async def broadcast(self, message: str, sender_id: int, room_id: int, session: AsyncSession):
        """
        Рассылает сообщение всем пользователям в комнате.
        """

        if room_id in self.active_connections:
            self_connection = ()
            is_read = False
            for user_id, connection in self.active_connections[room_id].items():
                if user_id == sender_id:
                    self_connection = (connection, )
                else:
                    is_read = True
                    message_with_class = {
                        "text": message,
                        "is_self": False,
                        "is_read": True
                    }
                    await connection.send_json(message_with_class)
                    await message_is_read(sender_id, room_id, session)
            if self_connection:
                connection = self_connection[0]
                message_with_class = {
                    "text": message,
                    "is_self": True,
                    "is_read": is_read
                }
                await connection.send_json(message_with_class)

async def create_chat(chat_data: ChatCreate, session: AsyncSession) -> int:
    chat_data = chat_data.model_dump(by_alias=True)
    chat = Chat(**chat_data)
    session.add(chat)
    await session.commit()
    return chat.id


async def get_chat(session: AsyncSession, chat_id: int | None = None):
    UserAssoc = aliased(UserChatAssociation)
    UserAlias = aliased(User)

    if chat_id:
        stmt = (
        select(Chat, UserAlias.id, UserAlias.name)
        .select_from(Chat)
        .join(UserAssoc, UserAssoc.chat_id == Chat.id, isouter=True)
        .join(UserAlias, UserAlias.id == UserAssoc.user_id, isouter=True)
        .join(Message, Message.chat_id == Chat.id, isouter=True).where(Chat.id == chat_id)
        .order_by(Message.timestamp.desc())
    )
    else:
        stmt = (
            select(Chat, UserAlias.id, UserAlias.name)
            .select_from(Chat)
            .join(UserAssoc, UserAssoc.chat_id == Chat.id, isouter=True)
            .join(UserAlias, UserAlias.id == UserAssoc.user_id, isouter=True)
            .join(Message, Message.chat_id == Chat.id, isouter=True)
            .order_by(Message.timestamp.desc())
        )
    result = await session.execute(stmt)
    rows = result.all()
    return [
        {
            "chat_id": chat.id,
            "chat_name": chat.name,
            "user_id": user_id,
            "user_name": user_name
        }
        for chat, user_id, user_name in rows
    ]

manager = ConnectionManager()
