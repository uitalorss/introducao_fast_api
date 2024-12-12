from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from cursos import courses
from models import Course

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item}")
async def get_item(item: str):
    return {"item": item}

@app.get("/cursos")
async def get_courses():
    return courses

@app.get("/cursos/{id}")
async def get_course(id: int):
    course = [item for item in courses if item["id"] == id]
    if course:
        return course[0]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado.')
    
@app.post("/cursos")
async def create_course(course: Course):
    course_in_list = [item for item in courses if item["id"] == course.id]
    if not course_in_list:
        courses.append(course)
        return {"message": "Curso cadastrado com sucesso."}
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Problema com relação a id do curso.")