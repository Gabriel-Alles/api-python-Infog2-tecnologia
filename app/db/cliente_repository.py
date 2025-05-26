from sqlalchemy.orm import Session
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate
from typing import Optional

def get_cliente(db: Session, cliente_id: int, user_id: int):
    return db.query(Cliente).filter(Cliente.id == cliente_id, Cliente.user_id == user_id).first()

def get_cliente_by_id(db: Session, cliente_id: int):
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()

def get_cliente_by_email(db: Session, email: str, user_id: int):
    return db.query(Cliente).filter(Cliente.email == email, Cliente.user_id == user_id).first()

def get_cliente_by_cpf(db: Session, cpf: str, user_id: int):
    return db.query(Cliente).filter(Cliente.cpf == cpf, Cliente.user_id == user_id).first()

def get_cliente_by_tel(db: Session, tel: str, user_id: int):
    return db.query(Cliente).filter(Cliente.tel == tel, Cliente.user_id == user_id).first()

def list_clientes(db: Session, user_id: int):
    return db.query(Cliente).filter(Cliente.user_id == user_id).all()

def list_all_clientes(db: Session):
    return db.query(Cliente).all()

def list_all_clientes_paginated(db: Session, skip: int, limit: int, nome: Optional[str], email: Optional[str]):
    query = db.query(Cliente)
    if nome:
        query = query.filter(Cliente.nome.ilike(f"%{nome}%"))
    if email:
        query = query.filter(Cliente.email.ilike(f"%{email}%"))
    return query.offset(skip).limit(limit).all()

def list_clientes_paginated(db: Session, user_id: int, skip: int, limit: int, nome: Optional[str], email: Optional[str]):
    query = db.query(Cliente).filter(Cliente.user_id == user_id)
    if nome:
        query = query.filter(Cliente.nome.ilike(f"%{nome}%"))
    if email:
        query = query.filter(Cliente.email.ilike(f"%{email}%"))
    return query.offset(skip).limit(limit).all()

def create_cliente(db: Session, cliente: ClienteCreate, user_id: int):
    db_cliente = Cliente(**cliente.dict(), user_id=user_id)
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def update_cliente(db: Session, db_cliente: Cliente, updates: ClienteUpdate):
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(db_cliente, field, value)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def delete_cliente(db: Session, db_cliente: Cliente):
    db.delete(db_cliente)
    db.commit()