from typing import Any
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.responses import JSONResponse
from cursos import courses
from course_models import Course
from routes import course_routes, default_routes
import create_tables

app = FastAPI(
    title='Introdução ao FastAPI',
    description='API de teste para estudo do FastAPI',
    version='0.0.1')

app.include_router(default_routes.router, tags=["default"])
app.include_router(course_routes.router, tags=["courses"])

if __name__ == '__main__':
    import asyncio

    asyncio.run(create_tables())