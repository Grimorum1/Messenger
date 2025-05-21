from datetime import datetime, UTC
from uuid import uuid4

from sqlalchemy import UUID, ForeignKey, Text, DateTime, Boolean
from sqlalchemy.orm import mapped_column, relationship

from chats.model import Chat
from db.base_model import Base


class Message(Base):
    id = mapped_column(UUID, primary_key=True, default=uuid4)
    chat_id = mapped_column(ForeignKey("chats.id"))
    sender_id = mapped_column(ForeignKey("users.id"))
    text = mapped_column(Text)
    timestamp = mapped_column(DateTime(timezone=True), default=datetime.now(UTC))
    is_read = mapped_column(Boolean, default=False)
    chat = relationship(Chat, back_populates="messages")
    sender = relationship("User", back_populates="sent_messages")
