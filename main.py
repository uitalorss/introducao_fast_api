from typing import Any
from fastapi import FastAPI, HTTPException, Response, Depends, status
from fastapi.responses import JSONResponse
from cursos import courses
from models import Course
from time import sleep


app = FastAPI(
    title='Introdução ao FastAPI',
    description='API de teste para estudo do FastAPI',
    version='0.0.1')

def fake_db():
    try:
        print("Abrindo conexão com banco de dados.")
        sleep(2)
    finally:
        print("fechando conexão com banco de dados.")
        sleep(2)

@app.get("/", tags=['intro'])
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item}", tags=['courses'])
async def get_item(item: str):
    return {"item": item}

@app.get("/cursos", tags=['courses'])
async def get_courses(db: Any = Depends(fake_db)):
    return courses

@app.get("/cursos/{id}", tags=['courses'])
async def get_course(id: int):
    course = [item for item in courses if item["id"] == id]
    if course:
        item = course
        return item
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado.')
    
@app.post("/cursos", tags=['courses'], status_code=status.HTTP_201_CREATED)
async def create_course(course: Course):
    course_in_list = [item for item in courses if item["id"] == course.id]
    if not course_in_list:
        courses.append(course)
        return {"message": "Curso cadastrado com sucesso."}
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Problema com relação a id do curso.")
    
@app.put("/cursos/{course_id}", tags=['courses'])
async def update_course(course_id: int, course: Course):
    for item in courses:
        if item["id"] == course_id:
            item["title"] = course.title
            item["lesson"] = course.lesson
            item["hour"] = course.hour
            return {"message": "Atualizado!!"}

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Curso não encontrado.")
    
@app.delete("/cursos/{course_id}", tags=['courses'])
async def delete_course(course_id: int):
    item_to_remove = next((item for item in courses if item["id"] == course_id), None)
    if not item_to_remove:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado.')
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)