from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from enum import Enum
from app.schemas.produto import ProdutoResponse
class PedidoStatusEnum(str, Enum):
    pendente = "pendente"
    enviado = "enviado"
    cancelado = "cancelado"


class PedidoItemCreate(BaseModel):
    produto_id: int
    quantidade: int = Field(..., gt=0)


class PedidoItemResponse(BaseModel):
    produto: ProdutoResponse
    quantidade: int

    class Config:
        from_attributes = True


class PedidoBase(BaseModel):
    cliente_id: int
    status: PedidoStatusEnum = PedidoStatusEnum.pendente
    itens: List[PedidoItemCreate]


class PedidoCreate(PedidoBase):
    pass


class PedidoUpdate(BaseModel):
    status: Optional[PedidoStatusEnum] = None


class PedidoResponse(BaseModel):
    id: int
    cliente_id: int
    status: PedidoStatusEnum
    itens: List[PedidoItemResponse]

    class Config:
        from_attributes = True

class PedidoStatusResponse(BaseModel):
    id: int
    status: str