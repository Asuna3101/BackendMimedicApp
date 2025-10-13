"""
API MimedicApp (login + agenda) con CORS para Flutter Web
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.config import settings
from app.core.database import engine
from app.models.base import Base
import app.models  # registra TODOS los modelos en el metadata

from app.api.v1.endpoints import api_router

# Crear tablas (solo dev; en prod usa Alembic)
Base.metadata.create_all(bind=engine)

# Instancia FastAPI
app = FastAPI(
    title="MimedicApp API",
    version=settings.PROJECT_VERSION,
    description="API de autenticación y agenda médica",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1|10\.0\.2\.2|192\.168\.\d+\.\d+)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],      # Authorization, Content-Type, etc.
    expose_headers=["*"],
    max_age=600,
)

# Habilitar Private Network Access para 192.168.x.x (Chrome)
class PrivateNetworkMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if request.headers.get("access-control-request-private-network", "").lower() == "true":
            response.headers["Access-Control-Allow-Private-Network"] = "true"
        return response

app.add_middleware(PrivateNetworkMiddleware)

# ⬇️ Monta SOLO el api_router con el prefijo de versión
app.include_router(api_router, prefix=settings.API_V1_STR)

# Ping
@app.get("/")
def read_root():
    return {
        "message": "MimedicApp API",
        "version": settings.PROJECT_VERSION,
        "docs": "/docs",
        "login_endpoint": f"{settings.API_V1_STR}/auth/login",
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "api", "version": settings.PROJECT_VERSION}
