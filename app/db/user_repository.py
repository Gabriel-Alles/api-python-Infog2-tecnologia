from sqlalchemy.orm import Session
from app.models.user import User

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_all_users(db: Session):
    return db.query(User).all()

def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()

