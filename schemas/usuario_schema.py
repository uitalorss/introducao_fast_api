from typing import Optional, List
from pydantic import BaseModel as SCBasemodel, EmailStr

from schemas.artigo_schema import ArtigoSchema

class UsuarioSchemaBase(SCBasemodel):
    id: Optional[int] = None
    nome: str
    email: EmailStr
    is_admin: bool = False

    class Config:
        orm_mode = True

class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha: str

    class Config:
        orm_mode = True

class UsuarioSchemaListArtigos(UsuarioSchemaBase):
    artigos: Optional[List[ArtigoSchema]]

class UsuarioSchemaUpdate(UsuarioSchemaBase):
    nome: Optional[str]
    email: Optional[EmailStr]
    senha: Optional[str]
    is_admin: Optional[bool]
