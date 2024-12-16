from typing import ClassVar
from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
import os
import dotenv

dotenv.load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: ClassVar[str] = "/api/v1"
    DB_URL: ClassVar[str] = "sqlite+aiosqlite:///./dev.db" #'postgresql+asyncpg://postgres:postgres@localhost:5432/faculdade'
    DBBaseModel: ClassVar[DeclarativeMeta] = declarative_base()

    JWT_KEY: str = os.getenv("JWT_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8

    class Config:
        case_sensitive: True

settings: Settings = Settings()