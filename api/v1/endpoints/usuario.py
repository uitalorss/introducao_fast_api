from typing import List
from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchemaBase, UsuarioSchemaCreate, UsuarioSchemaListArtigos, UsuarioSchemaUpdate

from core.auth.dependences import get_session, obter_usuario_atual
from core.auth.security import gera_hash_senha
from core.auth.auth import autenticar, criar_acesso_token

router = APIRouter()

@router.get("/logado", response_model=UsuarioSchemaBase)
async def get_usuario_logado(usuario_logado: UsuarioModel = Depends(obter_usuario_atual)):
    return usuario_logado

@router.get("/", response_model=List[UsuarioSchemaBase])
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios = result.scalars().unique().all()

        return usuarios

@router.get("/{usuario_id}", response_model=UsuarioSchemaListArtigos, status_code=status.HTTP_200_OK)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioSchemaListArtigos  = result.scalars().unique().one_or_none()

        if usuario is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")
        
        return usuario


@router.post("/", response_model=UsuarioSchemaBase, status_code=status.HTTP_201_CREATED)
async def post_usuario(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    novo_usuario: UsuarioModel = UsuarioModel(nome=usuario.nome, email=usuario.email, senha=gera_hash_senha(usuario.senha), is_admin=usuario.is_admin)

    async with db as session:
        try:
            session.add(novo_usuario)
            await session.commit()

            return novo_usuario
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email informado já cadastrado.")

    
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await autenticar(email=form_data.username, senha=form_data.password, db=db)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email e/ou senha incorretos")
    
    return JSONResponse(content={"access_token": criar_acesso_token(sub=usuario.id), "token_type": "bearer"}, status_code=status.HTTP_200_OK)
    
@router.put("/{usuario_id}", response_model=UsuarioSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario(usuario_id: int, usuario: UsuarioSchemaUpdate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        update_usuario: UsuarioSchemaBase = result.scalars().unique().one_or_none()

        if update_usuario is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")
        
        try:
            if usuario.nome:
                update_usuario.nome = usuario.nome
            if usuario.email:
                update_usuario.email = usuario.email
            if usuario.senha:
                update_usuario.senha = gera_hash_senha(usuario.senha)
            if usuario.is_admin:
                update_usuario.is_admin = usuario.is_admin

            await session.commit()

            return update_usuario
        
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email informado já cadastrado.")
    
@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: int, db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        delete_usuario: UsuarioSchemaBase = result.scalars().unique().one_or_none

        if delete_usuario is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")
        
        await session.delete(delete_usuario)
        await session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
