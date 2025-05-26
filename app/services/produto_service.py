from sqlalchemy.orm import Session
from app.schemas.produto import ProdutoCreate, ProdutoUpdate, ProdutoResponse
from app.models.produto import Produto
from app.db import produto_repository
from typing import Optional


def criar_produto_service(db: Session, produto_data: ProdutoCreate) -> Produto:
    return produto_repository.create_produto(db, produto_data)


def buscar_produto_service(db: Session, produto_id: int) -> ProdutoResponse | None:
    return produto_repository.get_produto(db, produto_id)

def listar_produtos_service(db: Session, skip: int, limit: int, categoria: Optional[str] = None, preco: Optional[str] = None, disponibilidade: Optional[str] = None):
    return produto_repository.list_produtos(db, skip, limit, categoria, preco, disponibilidade)


def atualizar_produto_service(db: Session, produto_id: int, updates: ProdutoUpdate):
    produto = produto_repository.get_produto(db, produto_id)
    if not produto:
        raise Exception("Produto não encontrado")

    produto_atualizado = {
        "id": produto_id,
        "descricao": updates.descricao,
        "valor": updates.valor,
        "codigo_barras": updates.codigo_barras,
        "secao": updates.secao,
        "estoque": updates.estoque,
        "data_validade": updates.data_validade,
        "imagens": updates.imagens or [],  # garantir lista vazia se None ou vazio
    }
    return produto_repository.update_produto(db, produto_atualizado)



def deletar_produto_service(db: Session, produto_id: int) -> bool:   
    return produto_repository.delete_produto(db, produto_id)
