from fastapi import APIRouter

from .endpoints import artigo

api_artigos = APIRouter()

api_artigos.include_router(artigo.router, prefix="/artigos", tags=["Artigos"])