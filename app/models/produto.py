from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from app.db.database import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, nullable=False)
    valor = Column(Float, nullable=False)
    codigo_barras = Column(String, unique=True, nullable=False)
    secao = Column(String, nullable=False)
    estoque = Column(Integer, nullable=False)
    data_validade = Column(Date, nullable=True)
    imagens = Column(String, nullable=True)

    pedido_items = relationship("PedidoItem", back_populates="produto")