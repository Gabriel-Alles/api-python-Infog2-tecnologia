from fastapi import Depends, HTTPException, status
from app.services.auth_service import get_current_user
from app.models.user import User, UserRole

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito ao administrador."
        )
    return current_user
