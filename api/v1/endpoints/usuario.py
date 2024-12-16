from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession

from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioSchemaBase, UsuarioSchemaCreate, UsuarioSchemaListArtigos, UsuarioSchemaUpdate
from services.usuario_service import criar_usuario, pegar_usuario, pegar_todos_usuarios, atualizar_usuario, deletar_usuario

from core.auth.dependences import get_session, obter_usuario_atual
from core.auth.auth import autenticar, criar_acesso_token

router = APIRouter()

@router.get("/logado", response_model=UsuarioSchemaBase)
async def get_usuario_logado(usuario_logado: UsuarioModel = Depends(obter_usuario_atual)):
    return usuario_logado

@router.get("/", response_model=List[UsuarioSchemaBase])
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    return await pegar_todos_usuarios(db)

@router.get("/{usuario_id}", response_model=UsuarioSchemaListArtigos, status_code=status.HTTP_200_OK)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    return await pegar_usuario(usuario_id, db)


@router.post("/", response_model=UsuarioSchemaBase, status_code=status.HTTP_201_CREATED)
async def post_usuario(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    return await criar_usuario(usuario, db)

    
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await autenticar(email=form_data.username, senha=form_data.password, db=db)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email e/ou senha incorretos")

    return JSONResponse(content={"access_token": criar_acesso_token(sub=usuario.id), "token_type": "bearer"}, status_code=status.HTTP_200_OK)
    
@router.put("/{usuario_id}", response_model=UsuarioSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario(usuario_id: int, usuario: UsuarioSchemaUpdate, db: AsyncSession = Depends(get_session)):
    return await atualizar_usuario(usuario_id, usuario, db)
    
@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: int, db:AsyncSession = Depends(get_session)):
    return await deletar_usuario(usuario_id, db)
