from sqlalchemy.orm import Session
from app.schemas.pedido import PedidoCreate
from app.models.pedido import Pedido, PedidoItem
from app.models.produto import Produto
from sqlalchemy.exc import NoResultFound
from typing import Optional
from sqlalchemy.orm import joinedload

def create_pedido(db: Session, pedido_data: PedidoCreate) -> Pedido:
    print(pedido_data)
    pedido = Pedido(cliente_id=pedido_data.cliente_id, status=pedido_data.status)
    db.add(pedido)
    db.flush()  # gera id para pedido
    
    # criar os itens
    for item in pedido_data.itens:
        produto = db.query(Produto).filter(Produto.id == item.produto_id).first()
        if not produto:
            raise ValueError(f"Produto id {item.produto_id} não encontrado")
        if produto.estoque < item.quantidade:
            raise ValueError(f"Estoque insuficiente para o produto {produto.descricao}")
        
        produto.estoque -= item.quantidade
        
        pedido_item = PedidoItem(
            pedido_id=pedido.id,
            produto_id=item.produto_id,
            quantidade=item.quantidade,
        )
        db.add(pedido_item)
    
    db.commit()
    db.refresh(pedido)

    # Converter imagens dos produtos em cada item
    for item in pedido.itens:
        if isinstance(item.produto.imagens, str):
            item.produto.imagens = item.produto.imagens.split(",") if item.produto.imagens else []

    return pedido



def get_pedido(db: Session, pedido_id: int) -> Optional[Pedido]:
    return db.query(Pedido).options(
        joinedload(Pedido.itens).joinedload(PedidoItem.produto)
    ).filter(Pedido.id == pedido_id).first()


def list_pedidos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Pedido).offset(skip).limit(limit).all()


def update_pedido(db: Session, pedido: Pedido, updates: dict):
    if "status" in updates:
        pedido.status = updates["status"]

    db.commit()
    db.refresh(pedido)
    return pedido


def delete_pedido(db: Session, pedido: Pedido):
    # Devolve os itens ao estoque antes de deletar
    for item in pedido.itens:
        produto = db.query(Produto).filter(Produto.id == item.produto_id).first()
        if produto:
            produto.estoque += item.quantidade
        db.delete(item)
    db.delete(pedido)
    db.commit()
