from fastapi import FastAPI
from core.config import settings
from api.v1.api import api_router

app = FastAPI(
    title='Introdução ao FastAPI',
    description='API de teste para estudo do FastAPI',
    version='0.0.1')

app.include_router(api_router, prefix=settings.API_V1_STR)