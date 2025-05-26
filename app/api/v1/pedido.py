from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from app.schemas.pedido import PedidoCreate, PedidoResponse, PedidoUpdate, PedidoStatusResponse
from app.services import pedido_service
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

@router.post("/", response_model=PedidoResponse)
def criar_pedido(pedido_data: PedidoCreate, db: Session = Depends(get_db)):
    return pedido_service.criar_pedido_service(db, pedido_data)

@router.get("/{pedido_id}")
def buscar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    return pedido_service.buscar_pedido_service(db, pedido_id)

@router.get("/")
def listar_pedidos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100), 
    db: Session = Depends(get_db),        
):
    return pedido_service.listar_pedidos_service(db=db, skip=skip, limit=limit)

@router.put("/{pedido_id}", response_model=PedidoStatusResponse)
def atualizar_pedido(pedido_id: int, updates: PedidoUpdate, db: Session = Depends(get_db)):
    response = pedido_service.atualizar_pedido_service(db, pedido_id, updates)
    if not response:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return response

@router.delete("/{pedido_id}")
def deletar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = pedido_service.buscar_pedido_service(db, pedido_id)
    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado")
    
    pedido_service.deletar_pedido_service(db, pedido_id)
    return {"message": "Pedido deletado com sucesso"}