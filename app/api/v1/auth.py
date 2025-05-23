from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.services.auth_service import authenticate_user, register_user, list_users
from app.schemas.user import UserCreate, UserLogin, Token, UserResponse
from app.core.security import create_access_token, create_refresh_token
from app.core.dependencies import require_admin

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user)

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return {
        "access_token": create_access_token({"sub": user.username}),
        "refresh_token": create_refresh_token({"sub": user.username})
    }

@router.get("/admin/users", response_model=list[UserResponse])
def get_all_users(current_user=Depends(require_admin)):
    return list_users()
