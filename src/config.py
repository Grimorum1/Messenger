from pydantic_settings import BaseSettings




class Settings(BaseSettings):
    db_url: str = "postgresql+asyncpg://postgres:postgres@db:5432/messenger"
    db_echo: bool = True


settings = Settings()
