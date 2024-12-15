from typing import Optional

from pydantic import BaseModel as SCBasemodel, HttpUrl

class ArtigoSchema(SCBasemodel):
    id: Optional[int] = None
    titulo: str
    descricao: str
    url_fonte: HttpUrl

    class Config:
        orm_mode = True