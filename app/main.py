from fastapi import FastAPI
from app.api.v1 import auth
from app.db.database import Base
from app.db.database import engine

app = FastAPI()
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])

Base.metadata.create_all(bind=engine)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)