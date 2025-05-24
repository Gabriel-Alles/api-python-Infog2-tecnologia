from fastapi import APIRouter, Depends, HTTPException
from app.db.database import SessionLocal
from app.core.security import require_admin
from app.services.auth_service import list_users  # exemplo
from app.schemas.user import UserResponse
from sqlalchemy.orm import Session

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db), current_user=Depends(require_admin)):
    return list_users(db)

@router.get("/admin-only")
def protected_route(current_user=Depends(require_admin)):
    return {"message": "Você é um administrador!"}
