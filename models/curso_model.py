from core.config import settings
from sqlalchemy import Integer, String, Column

class CursoModel(settings.DBBaseModel):
    __tablename__ = 'cursos'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    title: str = Column(String(100))
    lesson: int = (Column(Integer))
    hour: int = (Column(Integer))
    