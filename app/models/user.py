from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.db.database import Base
import enum

class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)  # Added email column
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)

    clientes = relationship("Cliente", back_populates="user")