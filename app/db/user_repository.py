from sqlalchemy.orm import Session
from app.models.user import User

def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_all_users(db: Session):
    return db.query(User).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: int, updates: dict) -> User | None:
    user = get_user(db, user_id)
    if not user:
        return None

    for key, value in updates.items():
        if hasattr(user, key):
            setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int) -> bool:
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

def get_all_users_paginated(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()

