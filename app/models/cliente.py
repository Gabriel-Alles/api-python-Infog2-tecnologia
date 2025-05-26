from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    cpf = Column(String, unique=True, index=True, nullable=False)
    tel = Column(String, unique=True, index=True, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    pedidos = relationship("Pedido", back_populates="cliente")
    user = relationship("User", back_populates="clientes")  # Added to match User model