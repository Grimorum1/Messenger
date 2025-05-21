from pydantic import BaseModel, Field
from enum import Enum

class ChatType(str, Enum):
    private = "private"
    group = "group"

class ChatCreate(BaseModel):
    name: str
    type_: ChatType = Field(..., alias='type')
