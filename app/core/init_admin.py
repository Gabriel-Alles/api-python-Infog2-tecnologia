from app.db.database import SessionLocal
from app.models.user import User, UserRole
from app.core.security import hash_password
from sqlalchemy.orm import Session
from app.core.config import settings
def init_admin_user():
    db: Session = SessionLocal()
    try:
        admin_username = settings.ADMIN_USERNAME
        admin_email = settings.ADMIN_EMAIL
        admin_password = settings.ADMIN_PASSWORD

        existing_user = db.query(User).filter(User.username == admin_username).first()
        if not existing_user:
            user = User(
                username=admin_username,
                email=admin_email,
                hashed_password=hash_password(admin_password),
                role=UserRole.ADMIN
            )
            db.add(user)
            db.commit()
            print("✅ Usuário admin criado com sucesso!")
        else:
            print("ℹ Usuário admin já existe.")
    finally:
        db.close()