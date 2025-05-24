from fastapi import FastAPI
from app.api.v1 import auth, admin
from app.db.database import Base
from app.db.database import engine
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, description="ConectaLu-API")
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])

Base.metadata.create_all(bind=engine)