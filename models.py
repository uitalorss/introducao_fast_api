from typing import Optional
from pydantic import BaseModel

class Course(BaseModel):
    id: Optional[int] = None
    title: str
    lesson: int
    hour: int

