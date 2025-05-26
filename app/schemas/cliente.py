from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class ClienteBase(BaseModel):
    nome: str
    email: EmailStr
    tel: Optional[str] = Field(
        None,
        pattern=r"^\d{10,11}$",
        description="Somente números: DDD + telefone (Ex: 11912345678 ou 1134567890)"
    )
    cpf: str = Field(..., pattern=r"^\d{11}$")  # Exactly 11 digits

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    tel: Optional[str] = None
    cpf: Optional[str] = Field(None, pattern=r"^\d{11}$")  # Optional, with pattern if provided

class ClienteResponse(ClienteBase):
    id: int

    class Config:
        from_attributes = True