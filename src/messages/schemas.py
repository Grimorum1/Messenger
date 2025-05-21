from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class MessageDelete(BaseModel):
    id: str | None = None
    chat_id: int | None = None



class MessageRead(BaseModel):
    id: UUID
    chat_id: int
    sender_id: int
    text: str
    timestamp: datetime
    is_read: bool

    class Config:
        orm_mode = True
