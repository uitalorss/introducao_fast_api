from typing import Optional

from pydantic import BaseModel as SCBasemodel

class CourseSchema(SCBasemodel):
    id: Optional[int]
    title: str
    lesson: int
    hour: int

    class Config:
        orm_mode = True