from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db.user_repository import (
    get_user_by_username,
    get_user_by_email,
    get_user,
    get_all_users,
    create_user,
    update_user,
    delete_user,
    get_all_users_paginated
)
from app.models.user import User, UserRole
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password


def register_user(db: Session, user_create: UserCreate):
    if get_user_by_username(db, user_create.username):
        raise HTTPException(status_code=400, detail="Username já cadastrado")
    if get_user_by_email(db, user_create.email):
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    hashed_pw = hash_password(user_create.password)
    new_user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_pw,
        role=UserRole.USER  # Força que todo novo usuário é USER
    )
    return create_user(db, new_user)


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def list_users(db: Session):
    return get_all_users(db)


def get_user_by_id_service(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


def get_user_by_email_service(db: Session, email: str):
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


def update_user_service(db: Session, user_id: int, updates: dict):
    user = update_user(db, user_id, updates)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado para atualização")
    return user


def delete_user_service(db: Session, user_id: int):
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Usuário não encontrado para exclusão")
    return {"message": "Usuário deletado com sucesso"}

def list_users_paginated(db: Session, skip: int = 0, limit: int = 10):
    return get_all_users_paginated(db, skip, limit)
