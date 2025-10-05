"""
API MimedicApp (login + agenda) con CORS para Flutter Web
"""
from fastapi import FastAPI                       # ← FALTABA
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.config import settings
from app.core.database import engine
from app.models import base
from app.api.v1.endpoints import auth, healthcare

# Crear tablas
base.Base.metadata.create_all(bind=engine)

# Instancia FastAPI
app = FastAPI(
    title="MimedicApp API",
    version=settings.PROJECT_VERSION,
    description="API de autenticación y agenda médica",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# CORS (sin allow_private_network, lo añadimos manualmente abajo)
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^http://(localhost|127\.0\.0\.1|192\.168\.\d+\.\d+)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],     # Authorization, Content-Type, etc.
    expose_headers=["*"],
    max_age=600,
)

# Habilitar Private Network Access para preflight de Chrome cuando llamas a 192.168.x.x
class PrivateNetworkMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if request.headers.get("access-control-request-private-network", "").lower() == "true":
            response.headers["Access-Control-Allow-Private-Network"] = "true"
        return response

app.add_middleware(PrivateNetworkMiddleware)      # ← FALTABA

# Routers
app.include_router(auth.router,       prefix=f"{settings.API_V1_STR}/auth",   tags=["authentication"])
app.include_router(healthcare.router, prefix=f"{settings.API_V1_STR}/health", tags=["health"])

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
