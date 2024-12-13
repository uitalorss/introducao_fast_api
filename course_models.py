from typing import Optional
from pydantic import BaseModel, field_validator

class Course(BaseModel):
    id: Optional[int] = None
    title: str
    lesson: int
    hour: int

    @field_validator('title')
    def validate_title(cls, value):
        title_to_validate = value.split(" ")

        if len(title_to_validate) < 3:
            raise ValueError("Nome do título deve ter pelo menos três palavras")
        
        return value
    
    @field_validator('lesson')
    def validate_lesson(cls, value):
        if value < 10:
            raise ValueError("Quantidade de aulas deve ser maior que 10.")
        
        return value
    
    @field_validator('hour')
    def validate_hour(cls, value):
        if value < 32:
            raise ValueError("Carga horária deve ser maior que 32 horas.")
        
        return value