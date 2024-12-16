from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.artigo_model import ArtigoModel
from models.usuario_model import UsuarioModel
from schemas.artigo_schema import ArtigoSchema, ArtigoSchemaUpdate
from core.auth.dependences import get_session, obter_usuario_atual

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ArtigoSchema)
async def post_artigo(artigo: ArtigoSchema, usuario_logado: UsuarioModel = Depends(obter_usuario_atual), db: AsyncSession = Depends(get_session)):
    novo_artigo: ArtigoModel = ArtigoModel(titulo=artigo.titulo, descricao=artigo.descricao, url_fonte=str(artigo.url_fonte), usuario_id=usuario_logado.id)

    db.add(novo_artigo)
    await db.commit()

    return novo_artigo

@router.get("/", response_model=List[ArtigoSchema])
async def get_artigos(db: AsyncSession = Depends(get_session)):
     async with db as session:
          query = select(ArtigoModel)
          result = await session.execute(query)
          artigos: List[ArtigoModel] = result.scalars().unique().all()

          return artigos
     
@router.get("/{artigo_id}", response_model=ArtigoSchema, status_code=status.HTTP_200_OK)
async def get_artigo(artigo_id:int, db: AsyncSession = Depends(get_session)):
     async with db as session:
          query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
          result = await session.execute(query)
          artigo: ArtigoModel = result.scalars().unique().one_or_none()

          if artigo is None:
               raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artigo não encontrado.")
          
          return artigo
     
@router.put("/{artigo_id}", response_model=ArtigoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_arigo(artigo_id: int, artigo: ArtigoSchemaUpdate, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(obter_usuario_atual)):
     async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        update_artigo: ArtigoModel = result.scalars().unique().one_or_none()

        if update_artigo is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artigo não encontrado.")
        
        if artigo.titulo:
            update_artigo.titulo = artigo.titulo

        if artigo.descricao:
            update_artigo.descricao = artigo.descricao
        
        if artigo.url_fonte:
            update_artigo.url_fonte = str(artigo.url_fonte)

        await session.commit()

        return update_artigo
     
@router.delete("/{artigo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artigo(artigo_id: int, usuario_logado: UsuarioModel = Depends(obter_usuario_atual), db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        delete_artigo: ArtigoModel = result.scalars().unique().one_or_none()

        if delete_artigo is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado.")
        
        await session.delete(delete_artigo)
        await session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    