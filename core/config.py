from typing import ClassVar
from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

class Settings(BaseSettings):
    API_V1_STR: ClassVar[str] = '/api/v1'
    DB_URL: ClassVar[str] = 'postgresql+asyncpg://postgres:postgres@localhost:5432/faculdade'
    DBBaseModel: ClassVar[DeclarativeMeta] = declarative_base()

    class config:
        case_sensitive: True

settings: Settings = Settings()