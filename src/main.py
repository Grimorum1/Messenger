from contextlib import asynccontextmanager

from fastapi import FastAPI

from db.base_model import Base
from db.db_setup import db_helper
from users.routers import router as user_router
from chats.routers import router as chat_router
from messages.routers import router as message_router
from groups.routers import router as group_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield



app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(chat_router)
app.include_router(message_router)
app.include_router(group_router)

