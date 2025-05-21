import logging

from pydantic_settings import BaseSettings




class Settings(BaseSettings):
    db_url: str = "postgresql+asyncpg://postgres:postgres@db:5432/messenger"
    db_echo: bool = True
    level_logger: str = 'INFO' #logging.INFO

settings = Settings()
