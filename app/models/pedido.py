from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import enum

class PedidoStatus(enum.Enum):
    pendente = "pendente"
    enviado = "enviado"
    cancelado = "cancelado"

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    status = Column(Enum(PedidoStatus), default=PedidoStatus.pendente)
    data_criacao = Column(Date, server_default=func.now())

    cliente = relationship("Cliente", back_populates="pedidos")
    itens = relationship("PedidoItem", back_populates="pedido", cascade="all, delete-orphan")

class PedidoItem(Base):
    __tablename__ = "pedido_itens"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)

    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto", back_populates="pedido_items")