from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.cliente import ClienteCreate, ClienteUpdate
from app.db import cliente_repository
from typing import Optional

def create_cliente(db: Session, cliente: ClienteCreate, user_id: int):
    if cliente_repository.get_cliente_by_email(db, cliente.email, user_id):
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    if cliente_repository.get_cliente_by_cpf(db, cliente.cpf, user_id):
        raise HTTPException(status_code=400, detail="CPF já cadastrado")
    if cliente_repository.get_cliente_by_tel(db, cliente.tel, user_id):
        raise HTTPException(status_code=400, detail="Telefone já cadastrado")
    return cliente_repository.create_cliente(db, cliente, user_id)

def get_cliente(db: Session, cliente_id: int, user_id: int):
    cliente = cliente_repository.get_cliente(db, cliente_id, user_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

def get_cliente_by_id(db: Session, cliente_id: int):
    cliente = cliente_repository.get_cliente_by_id(db, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

def list_clientes(db: Session, user_id: int):
    return cliente_repository.list_clientes(db, user_id)

def list_all_clientes(db: Session):
    return cliente_repository.list_all_clientes(db)

def update_cliente(db: Session, cliente_id: int, updates: ClienteUpdate):
    cliente = get_cliente_by_id(db, cliente_id)
    return cliente_repository.update_cliente(db, cliente, updates)

def delete_cliente(db: Session, cliente_id: int):
    cliente = get_cliente_by_id(db, cliente_id)
    cliente_repository.delete_cliente(db, cliente)

def list_all_clientes_paginated(db: Session, skip: int, limit: int, nome: Optional[str] = None, email: Optional[str] = None):
    return cliente_repository.list_all_clientes_paginated(db, skip, limit, nome, email)

def list_clientes_paginated(db: Session, user_id: int, skip: int, limit: int, nome: Optional[str] = None, email: Optional[str] = None):
    return cliente_repository.list_clientes_paginated(db, user_id, skip, limit, nome, email)
