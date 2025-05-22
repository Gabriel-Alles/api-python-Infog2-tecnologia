from app.db.user_repository import get_user_by_username, create_user
from app.core.security import verify_password, hash_password, create_access_token, create_refresh_token
from app.models.user import User
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session
from fastapi import HTTPException

def register_user(db: Session, user_create: UserCreate):
    if get_user_by_username(db, user_create.username):
        raise HTTPException(status_code=400, detail="Username já cadastrado")
    hashed_pw = hash_password(user_create.password)
    new_user = User(
        username=user_create.username,
        email=user_create.email,
        hashed_password=hashed_pw
    )
    return create_user(db, new_user)

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user  