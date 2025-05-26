from sqlalchemy.orm import Session
from app.schemas.produto import ProdutoCreate, ProdutoResponse
from app.models.produto import Produto
from sqlalchemy.exc import NoResultFound
from typing import Optional
import json

def create_produto(db: Session, produto_data: ProdutoCreate) -> Produto:
    produto = Produto(
        descricao=produto_data.descricao,
        valor=produto_data.valor,
        codigo_barras=produto_data.codigo_barras,
        secao=produto_data.secao,
        estoque=produto_data.estoque,
        data_validade=produto_data.data_validade,
        imagens=",".join(produto_data.imagens) if produto_data.imagens else None,
    )
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto


def get_produto(db: Session, produto_id: int) -> ProdutoResponse | None:
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        return None

    return ProdutoResponse(
        id=produto.id,
        descricao=produto.descricao,
        valor=produto.valor,
        codigo_barras=produto.codigo_barras,
        secao=produto.secao,
        estoque=produto.estoque,
        data_validade=produto.data_validade,
        imagens=produto.imagens.split(",") if produto.imagens else []
    )

def list_produtos(db: Session, skip: int, limit: int, categaria: Optional[str], preco: Optional[str], disponibilidade: Optional[str]):
    query = db.query(Produto)
    if categaria:
        query = query.filter(Produto.secao.ilike(f"%{categaria}%"))
    if preco:
        query = query.filter(Produto.valor >= float(preco))
    if disponibilidade:
        query = query.filter(Produto.estoque >= int(disponibilidade))

    produtos = query.offset(skip).limit(limit).all()

    for produto in produtos:
        if isinstance(produto.imagens, str):
            try:
                produto.imagens = json.loads(produto.imagens)
            except json.JSONDecodeError:
                produto.imagens = []  # fallback se for string vazia

    return produtos



def get_produto_orm(db: Session, produto_id: int) -> Optional[Produto]:
    return db.query(Produto).filter(Produto.id == produto_id).first()

def update_produto(db: Session, updates: dict):
    produto = db.query(Produto).filter(Produto.id == updates["id"]).first()
    if not produto:
        raise Exception("Produto não encontrado")

    for key, value in updates.items():
        if key == "imagens":
            # Se imagens for lista, converte para string antes de salvar
            if isinstance(value, list):
                value = ",".join(value)
        setattr(produto, key, value)

    db.commit()
    db.refresh(produto)

    # Retornar o objeto com imagens convertidas de volta para lista
    produto_dict = {
        "id": produto.id,
        "descricao": produto.descricao,
        "valor": produto.valor,
        "codigo_barras": produto.codigo_barras,
        "secao": produto.secao,
        "estoque": produto.estoque,
        "data_validade": produto.data_validade,
        "imagens": produto.imagens.split(",") if produto.imagens else []
    }
    return produto_dict

def delete_produto(db: Session, produto_id: int):
    db.delete(get_produto_orm(db, produto_id))
    return db.commit()
    