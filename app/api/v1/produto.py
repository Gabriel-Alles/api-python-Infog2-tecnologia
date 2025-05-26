from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.schemas.produto import ProdutoCreate, ProdutoResponse, ProdutoUpdate
from app.services import produto_service
from fastapi import Query
from typing import Optional

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ProdutoResponse)
def criar_produto(produto_data: ProdutoCreate, db: Session = Depends(get_db)):
    return produto_service.criar_produto_service(db, produto_data)


from fastapi import HTTPException

@router.get("/{produto_id}", response_model=ProdutoResponse)
def buscar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = produto_service.buscar_produto_service(db, produto_id)
    if produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto


@router.get("/", response_model=list[ProdutoResponse])
def listar_produtos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100), 
    db: Session = Depends(get_db),
    categoria: Optional[str] = Query(None),
    preco: Optional[str] = Query(None),
    disponibilidade: Optional[int] = Query(None),
    ):
    return produto_service.listar_produtos_service(db=db, skip=skip, limit=limit, categoria=categoria, preco=preco, disponibilidade=disponibilidade)


@router.put("/{produto_id}", response_model=ProdutoResponse)
def atualizar_produto(produto_id: int, updates: ProdutoUpdate, db: Session = Depends(get_db)):
    return produto_service.atualizar_produto_service(db, produto_id, updates)


@router.delete("/{produto_id}")
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = produto_service.buscar_produto_service(db, produto_id)
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")
    
    produto_service.deletar_produto_service(db, produto_id)
    return {"message": "Produto deletado com sucesso"}