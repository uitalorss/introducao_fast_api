from typing import List
from fastapi import status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.artigo_model import ArtigoModel
from models.usuario_model import UsuarioModel
from schemas.artigo_schema import ArtigoSchema, ArtigoSchemaUpdate

async def criar_artigo(artigo: ArtigoSchema, usuario_logado: UsuarioModel, db: AsyncSession):
    novo_artigo: ArtigoModel = ArtigoModel(titulo=artigo.titulo, descricao=artigo.descricao, url_fonte=str(artigo.url_fonte), usuario_id=usuario_logado.id)

    db.add(novo_artigo)
    await db.commit()

    return novo_artigo

async def listar_todos_artigos(db: AsyncSession):
    async with db as session:
        query = select(ArtigoModel)
        result = await session.execute(query)
        artigos: List[ArtigoModel] = result.scalars().unique().all()

        return artigos
    
async def pegar_artigo(artigo_id: int, db: AsyncSession):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo: ArtigoModel = result.scalars().unique().one_or_none()

        if artigo is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artigo não encontrado.")
        
        return artigo
    
async def atualizar_artigo(artigo_id: int, artigo: ArtigoSchema, db: AsyncSession):
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
    
async def deletar_artigo(artigo_id: int, db: AsyncSession):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        delete_artigo: ArtigoModel = result.scalars().unique().one_or_none()

        if delete_artigo is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado.")
        
        await session.delete(delete_artigo)
        await session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)