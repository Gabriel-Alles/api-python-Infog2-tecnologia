from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.core.security import hash_password
from app.core.config import settings
from app.db.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_admin_user(db: Session = None):
    if db is None:
        with next(get_db()) as db:
            create_admin_user(db)
    else:
        create_admin_user(db)

def create_admin_user(db: Session):
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
        print("ℹ️ Usuário admin já existe.")