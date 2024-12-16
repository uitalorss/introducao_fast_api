from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.artigo_model import ArtigoModel
from models.usuario_model import UsuarioModel
from schemas.artigo_schema import ArtigoSchema, ArtigoSchemaUpdate
from services.artigo_service import criar_artigo, listar_todos_artigos, pegar_artigo, atualizar_artigo, deletar_artigo

from core.auth.dependences import get_session, obter_usuario_atual

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ArtigoSchema)
async def post_artigo(artigo: ArtigoSchema, usuario_logado: UsuarioModel = Depends(obter_usuario_atual), db: AsyncSession = Depends(get_session)):
    return await criar_artigo(artigo, usuario_logado, db)

@router.get("/", response_model=List[ArtigoSchema])
async def get_artigos(db: AsyncSession = Depends(get_session)):
    return await listar_todos_artigos(db)
     
@router.get("/{artigo_id}", response_model=ArtigoSchema, status_code=status.HTTP_200_OK)
async def get_artigo(artigo_id:int, db: AsyncSession = Depends(get_session)):
    return await pegar_artigo(artigo_id, db)
     
@router.put("/{artigo_id}", response_model=ArtigoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_arigo(artigo_id: int, artigo: ArtigoSchemaUpdate, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(obter_usuario_atual)):
     return await atualizar_artigo(artigo_id, artigo, db)
     
@router.delete("/{artigo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artigo(artigo_id: int, usuario_logado: UsuarioModel = Depends(obter_usuario_atual), db: AsyncSession = Depends(get_session)):
    return await deletar_artigo(artigo_id, db)
    