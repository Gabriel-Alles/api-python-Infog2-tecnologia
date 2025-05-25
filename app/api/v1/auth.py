from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.services.auth_service import authenticate_user, register_user
from app.schemas.user import UserCreate, UserLogin, Token
from app.core.security import create_access_token, create_refresh_token
from fastapi import Request
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
        "refresh_token": create_refresh_token({"sub": user.username}),
    }

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user)

@router.post("/refresh-token", response_model=Token)
async def refresh_token(request: Request):
    data = await request.json()
    refresh_token = data.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=400, detail="Refresh token não fornecido")

    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Refresh token inválido")

    # Pegamos os dados do token antigo
    username = payload.get("sub")
    email = payload.get("email", "")
    role = payload.get("role", UserRole.USER.value)

    new_access_token = create_access_token({
        "sub": username,
        "email": email,
        "role": role,
    })

    return {
        "access_token": new_access_token,
        "refresh_token": refresh_token,  # ou gere outro novo, se quiser
        "token_type": "bearer"
    }