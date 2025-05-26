from pydantic import BaseModel, Field,  constr
from typing import List, Optional
from datetime import date
from enum import Enum

class ProdutoBase(BaseModel):
    descricao: Optional[str] = None
    valor: Optional[float] = None
    codigo_barras: Optional[str] = Field(None, min_length=1)
    secao: Optional[str] = None
    estoque: Optional[int] = Field(None, ge=0)
    data_validade: Optional[date] = None
    imagens: Optional[List[str]] = Field(default_factory=list)

    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        if d.get('imagens') is None:
            d['imagens'] = []
        return d


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoUpdate(BaseModel):
    descricao: Optional[str] = None
    valor: Optional[float] = None
    codigo_barras: Optional[str] = Field(None, min_length=1)
    secao: Optional[str] = None
    estoque: Optional[int] = Field(None, ge=0)
    data_validade: Optional[date] = None
    imagens: Optional[List[str]] = Field(default_factory=list)

    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        if d.get('imagens') is None:
            d['imagens'] = []
        return d


class ProdutoResponse(ProdutoBase):
    id: int

    class Config:
        from_attributes = True
