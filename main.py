from fastapi import FastAPI, HTTPException, Response, status
from fastapi.responses import JSONResponse
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
        item = course
        return item
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado.')
    
@app.post("/cursos", status_code=status.HTTP_201_CREATED)
async def create_course(course: Course):
    course_in_list = [item for item in courses if item["id"] == course.id]
    if not course_in_list:
        courses.append(course)
        return {"message": "Curso cadastrado com sucesso."}
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Problema com relação a id do curso.")
    
@app.put("/cursos/{course_id}")
async def update_course(course_id: int, course: Course):
    for item in courses:
        if item["id"] == course_id:
            item["title"] = course.title
            item["lesson"] = course.lesson
            item["hour"] = course.hour
            return {"message": "Atualizado!!"}

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Curso não encontrado.")
    
@app.delete("/cursos/{course_id}")
async def delete_course(course_id: int):
    item_to_remove = {}
    for item in courses:
        if(item["id"] == course_id):
            item_to_remove = item
    
    courses.remove(item_to_remove)
    return Response(status_code=status.HTTP_201_CREATED)