from fastapi import FastAPI
from app.api.v1 import auth, admin, cliente, pedido, produto
from app.db.database import Base, engine
from app.core.config import settings
from app.core.init_admin import init_admin_user
import os
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0,
    environment="production",
    send_default_pii=True
)

app = FastAPI(title=settings.PROJECT_NAME, description="API for ConectaLu")
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["users"])
app.include_router(cliente.router, prefix="/api/v1/cliente", tags=["clientes"])
app.include_router(pedido.router, prefix="/api/v1/pedido", tags=["pedidos"])
app.include_router(produto.router, prefix="/api/v1/produto", tags=["produtos"])

Base.metadata.create_all(bind=engine)

@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0

@app.on_event("startup")
def startup_event():
    init_admin_user()

@app.on_event("shutdown")
async def shutdown_event():
    pass