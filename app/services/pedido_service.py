from sqlalchemy.orm import Session
from app.schemas.pedido import PedidoCreate, PedidoUpdate
from app.models.pedido import Pedido
from app.db import pedido_repository
from typing import Optional


def criar_pedido_service(db: Session, pedido_data: PedidoCreate) -> Pedido:
    return pedido_repository.create_pedido(db, pedido_data)


def buscar_pedido_service(db: Session, pedido_id: int) -> Optional[Pedido]:
    return pedido_repository.get_pedido(db, pedido_id)


def listar_pedidos_service(db: Session, skip: int = 0, limit: int = 10):
    return pedido_repository.list_pedidos(db, skip, limit)


def atualizar_pedido_service(db: Session, pedido_id: int, updates: PedidoUpdate) -> Optional[dict]:
    pedido = pedido_repository.get_pedido(db, pedido_id)
    if not pedido:
        return None

    update_data = updates.dict(exclude_unset=True)
    print("Payload final:", update_data)

    pedido_atualizado = pedido_repository.update_pedido(db, pedido, update_data)

    return {"id": pedido_atualizado.id, "status": pedido_atualizado.status}


def deletar_pedido_service(db: Session, pedido_id: int) -> bool:
    pedido = pedido_repository.get_pedido(db, pedido_id)
    if not pedido:
        return False
    pedido_repository.delete_pedido(db, pedido)
    return True
