from fastapi import APIRouter

from api.v1.endpoints import curso, usuario, artigo

api_router = APIRouter()

api_router.include_router(curso.router, prefix="/cursos", tags=["Cursos"])
api_router.include_router(usuario.router, prefix="/usuarios", tags=["Usuários"])
api_router.include_router(artigo.router, prefix="/artigos", tags=["Artigos"])