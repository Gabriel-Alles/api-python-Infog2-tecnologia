from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings  # seu arquivo de config

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True  # ✅ adiciona essa opção
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
