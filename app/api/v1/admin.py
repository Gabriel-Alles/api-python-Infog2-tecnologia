from fastapi import APIRouter, Depends, HTTPException, Path, Body
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.core.security import require_admin
from app.schemas.user import UserResponse, UserUpdate
from app.services.auth_service import (
    list_users,
    get_user_by_id_service,
    update_user_service,
    delete_user_service,
)

router = APIRouter()

# Dependência para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ Listar todos os usuários
@router.get("/users", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db), current_user=Depends(require_admin)):
    return list_users(db)


# ✅ Obter usuário por ID
@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db), current_user=Depends(require_admin)):
    return get_user_by_id_service(db, user_id)


# ✅ Atualizar usuário
@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, updates: UserUpdate, db: Session = Depends(get_db), current_user=Depends(require_admin)):
    update_data = updates.dict(exclude_unset=True)
    if "password" in update_data:
        from app.core.security import hash_password
        update_data["hashed_password"] = hash_password(update_data.pop("password"))
    return update_user_service(db, user_id, update_data)


# ✅ Deletar usuário
@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(require_admin)):
    return delete_user_service(db, user_id)


# ✅ Exemplo simples de rota protegida para admin
@router.get("/admin-only")
def protected_route(current_user=Depends(require_admin)):
    return {"message": "Você é um administrador!"}