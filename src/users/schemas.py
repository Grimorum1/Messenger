from pydantic import BaseModel, EmailStr




class UserBase(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
