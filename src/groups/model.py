from sqlalchemy import Integer, String, ForeignKey, ARRAY
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import mapped_column

from db.base_model import Base


class Group(Base):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    members_list = mapped_column(MutableList.as_mutable(ARRAY(Integer)))
    creator_id = mapped_column(ForeignKey("users.id"))





