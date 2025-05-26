from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.cliente import ClienteCreate, ClienteResponse, ClienteUpdate
from app.services import cliente_service
from app.core.security import get_current_user # middleware de autenticação
from app.models.user import User, UserRole
from app.models.cliente import Cliente
from app.db.database import SessionLocal
from fastapi import Query
from typing import Optional

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_permission(cliente, current_user: User):
    if current_user.role != UserRole.ADMIN and cliente.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissão negada")

@router.post("/", response_model=ClienteResponse)
def create(
    cliente: ClienteCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    print(current_user.id)
    return cliente_service.create_cliente(db, cliente, current_user.id)

@router.get("/", response_model=list[ClienteResponse])
def list_all(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    nome: Optional[str] = Query(None),
    email: Optional[str] = Query(None)
):
    if current_user.role == UserRole.ADMIN:
        return cliente_service.list_all_clientes_paginated(
            db, skip=skip, limit=limit, nome=nome, email=email
        )
    else:
        return cliente_service.list_clientes_paginated(
            db, user_id=current_user.id, skip=skip, limit=limit, nome=nome, email=email
        )
       
@router.get("/{cliente_id}", response_model=ClienteResponse)
def get(cliente_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cliente = cliente_service.get_cliente_by_id(db, cliente_id)
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado")
    check_permission(cliente, current_user)
    return cliente

@router.put("/{cliente_id}", response_model=ClienteResponse)
def update(cliente_id: int, updates: ClienteUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cliente = cliente_service.get_cliente_by_id(db, cliente_id)
    print(cliente.id)
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado")
    check_permission(cliente, current_user)
    updated = cliente_service.update_cliente(db, cliente_id, updates)
    return updated

@router.delete("/{cliente_id}")
def delete(cliente_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cliente = cliente_service.get_cliente_by_id(db, cliente_id)
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado")
    check_permission(cliente, current_user)
    cliente_service.delete_cliente(db, cliente_id)
    return {"message": "Cliente deletado com sucesso"}
