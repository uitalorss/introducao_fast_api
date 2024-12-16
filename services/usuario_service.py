from fastapi import HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from core.auth.security import gera_hash_senha

from models.usuario_model import UsuarioModel

from schemas.usuario_schema import UsuarioSchemaBase, UsuarioSchemaCreate, UsuarioSchemaListArtigos, UsuarioSchemaUpdate

async def criar_usuario(usuario: UsuarioSchemaCreate, db:AsyncSession):
    novo_usuario: UsuarioModel = UsuarioModel(nome=usuario.nome, email=usuario.email, senha=gera_hash_senha(usuario.senha), is_admin=usuario.is_admin)

    async with db as session:
        try:
            session.add(novo_usuario)
            await session.commit()

            return novo_usuario
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email informado já cadastrado.")

async def pegar_usuario(usuario_id: int, db: AsyncSession):
     async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioSchemaListArtigos  = result.scalars().unique().one_or_none()

        if usuario is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")
        
        return usuario
     
async def pegar_todos_usuarios(db: AsyncSession):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios = result.scalars().unique().all()

        return usuarios
    
async def atualizar_usuario(usuario_id: int, usuario: UsuarioSchemaUpdate, db: AsyncSession):
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
        
async def deletar_usuario(usuario_id: int, db:AsyncSession):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        delete_usuario: UsuarioSchemaBase = result.scalars().unique().one_or_none()

        if delete_usuario is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")
        
        await session.delete(delete_usuario)
        await session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)