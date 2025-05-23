from asyncio import current_task
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session, AsyncSession

from config import settings


class DataBase:

    def __init__(self, db_url: str, echo: bool = False):
        print(f"Создаем подключение к {db_url = }")
        self.engine = create_async_engine(
            url=db_url,
            echo=echo
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
            autocommit=False
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncGenerator[AsyncSession, Any]:
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(self) -> AsyncGenerator[async_scoped_session[AsyncSession | Any], Any]:
        session = self.get_scoped_session()
        yield session
        await session.close()



db_helper = DataBase(db_url=settings.db_url, echo=settings.db_echo)