from fastapi import APIRouter

from .endpoints import usuario

api_usuarios = APIRouter()

api_usuarios.include_router(usuario.router, prefix="/usuarios", tags=["Usuários"])