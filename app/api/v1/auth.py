from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.services.auth_service import authenticate_user, register_user
from app.schemas.user import UserCreate, UserLogin
from app.schemas.token import Token, RefreshTokenRequest
from app.core.security import create_access_token, create_refresh_token
from app.core.security import decode_token
from app.models.user import UserRole

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    print(user.username, user.email, user.role.value)
    return {
        "access_token": create_access_token({
            "sub": user.username,
            "email": user.email,
            "role": user.role.value  # Converte o Enum para string
        }),
        "refresh_token": create_refresh_token({
            "sub": user.username,
            "email": user.email,
            "role": user.role.value
        })
    }

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user)

@router.post("/refresh-token", response_model=Token)
def refresh_token(payload: RefreshTokenRequest):
    token = payload.refresh_token

    decoded = decode_token(token)
    if not decoded or decoded.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Refresh token inválido")

    username = decoded.get("sub")
    email = decoded.get("email", "")
    role = decoded.get("role", UserRole.USER.value)

    return {
        "access_token": create_access_token({
            "sub": username,
            "email": email,
            "role": role
        }),
        "refresh_token": token,
        "token_type": "bearer"
    }