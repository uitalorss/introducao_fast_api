from typing import AsyncGenerator, Optional
from fastapi import Depends, HTTPException, status
import jwt
from jwt import PyJWTError


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from core.database import Session
from core.auth.auth import oauth_schema
from core.config import settings
from models.usuario_model import UsuarioModel

async def get_session() -> AsyncGenerator:
    session: AsyncSession = Session()

    try:
        yield session
    finally:
        await session.close()

async def obter_usuario_atual(
        db: AsyncSession = Depends(get_session), 
        token: str = Depends(oauth_schema)) -> UsuarioModel:
    
    credential_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token de acesso inválido ou expirado.",
        headers={"WWW-authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False}
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise credential_exception
        
    except PyJWTError:
        raise credential_exception
    
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == int(user_id))
        result = await session.execute(query)
        usuario: UsuarioModel = result.scalars().unique().one_or_none()

        if usuario is None:
            raise credential_exception
        
        return usuario
