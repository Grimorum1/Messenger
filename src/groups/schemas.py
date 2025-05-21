from pydantic import BaseModel


class GroupCreate(BaseModel):
    name: str
    creator_id: int
    members_list: list[int] | None = None


class GroupAddUser(BaseModel):
    group_id: int
    user_id: int