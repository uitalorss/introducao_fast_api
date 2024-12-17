from fastapi import FastAPI
from core.config import settings
from modules.artigos import artigos_routes
from modules.usuarios import usuarios_routes

app = FastAPI(
    title='Introdução ao FastAPI',
    description='API de teste para estudo do FastAPI',
    version='0.0.1')

app.include_router(artigos_routes.api_artigos, prefix=settings.API_V1_STR)
app.include_router(usuarios_routes.api_usuarios, prefix=settings.API_V1_STR)