from fastapi import FastAPI, HTTPException, Response, Depends, APIRouter, status
from typing import Any
from cursos import courses
from course_models import Course
from time import sleep


router = APIRouter()

@router.get("/cursos")
async def get_courses():
    return courses

@router.get("/cursos/{id}")
async def get_course(id: int):
    course = [item for item in courses if item["id"] == id]
    if course:
        item = course
        return item
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado.')
    
@router.post("/cursos", status_code=status.HTTP_201_CREATED)
async def create_course(course: Course):
    course_in_list = [item for item in courses if item["id"] == course.id]
    if not course_in_list:
        courses.append(course)
        return {"message": "Curso cadastrado com sucesso."}
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Problema com relação a id do curso.")
    
@router.put("/cursos/{course_id}")
async def update_course(course_id: int, course: Course):
    for item in courses:
        if item["id"] == course_id:
            item["title"] = course.title
            item["lesson"] = course.lesson
            item["hour"] = course.hour
            return {"message": "Atualizado!!"}

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Curso não encontrado.")
    
@router.delete("/cursos/{course_id}")
async def delete_course(course_id: int):
    item_to_remove = next((item for item in courses if item["id"] == course_id), None)
    if item_to_remove is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Curso não encontrado.')
    
    courses.remove(item_to_remove)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)