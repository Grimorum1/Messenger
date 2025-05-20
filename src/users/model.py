from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column

from db.base_model import Base


class User(Base):
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String)
    email = mapped_column(String, unique=True)
    password = mapped_column(String)