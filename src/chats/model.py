from datetime import datetime, UTC

from sqlalchemy import Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import mapped_column, relationship

from db.base_model import Base


class Chat(Base):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    type = mapped_column("type", Enum("private", "group", name="chat_type"))
    messages = relationship(
        "Message",
        back_populates="chat",
        cascade="all, delete-orphan",
    )
    members = relationship(
        "UserChatAssociation",
        back_populates="chat",
        cascade="all, delete-orphan"
    )



class UserChatAssociation(Base):
    __tablename__ = "user_chat_association"

    user_id = mapped_column(ForeignKey("users.id"), primary_key=True)
    chat_id = mapped_column(ForeignKey("chats.id"), primary_key=True)
    joined_at = mapped_column(DateTime, default=datetime.now(UTC))

    # Связи
    user = relationship("User", back_populates="chats")
    chat = relationship("Chat", back_populates="members")