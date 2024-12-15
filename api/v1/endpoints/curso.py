from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.curso_model import CursoModel
from schemas.course_schema import CourseSchema
from core.dependences import get_session

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CourseSchema)
async def post_curso(curso: CourseSchema, db: AsyncSession = Depends(get_session)):
    novo_curso = CursoModel(title=curso.title, lesson=curso.lesson, hour=curso.hour)

    db.add(novo_curso)
    await db.commit()
    return novo_curso

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[CourseSchema])
async def get_cursos(db: AsyncSession = Depends(get_session)):
        async with db as session:
              query = select(CursoModel)
              result = await session.execute(query)
              cursos: List[CursoModel] = result.scalars().all()

              return cursos
        
@router.get("/{course_id}", status_code=status.HTTP_200_OK, response_model=CourseSchema)
async def get_curso_by_id(curso_id: int, db: AsyncSession = Depends(get_session)):
      async with db as session:
            query = select(CursoModel).filter(CursoModel.id == curso_id)
            result = await session.execute(query)
            curso = result.scalar_one_or_none()

            if curso is None:
                  raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado!")
            
            return curso
      
@router.put("/{curso_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_curso(curso_id: int, curso: CourseSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso_update = result.scalar_one_or_none()

        if curso_update is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado!")
        
        curso_update.title = curso.title
        curso_update.lesson = curso.lesson
        curso_update.hour = curso.hour

        await session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.delete("/{curso_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(curso_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso_delete = result.scalar_one_or_none()

        if curso_delete is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado!")
        
        await session.delete(curso_delete)

        return Response(status_code=status.HTTP_204_NO_CONTENT)