"""
API de Login - Backend simplificado solo para autenticación
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.endpoints import auth
from app.core.database import engine
from app.models import base
from app.api.v1.endpoints import healthcare

# Crear tablas en la base de datos
base.Base.metadata.create_all(bind=engine)

# Crear instancia de FastAPI
app = FastAPI(
    title="MimedicApp Login API",
    version=settings.PROJECT_VERSION,
    description="API simplificada solo para login/autenticación",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir solo router de autenticación
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["authentication"])
app.include_router(healthcare.router, prefix=f"{settings.API_V1_STR}/health", tags=["health"]) 

@app.get("/")
def read_root():
    """Endpoint raíz"""
    return {
        "message": "MimedicApp Login API",
        "version": settings.PROJECT_VERSION,
        "description": "API simplificada solo para login",
        "docs": "/docs",
        "login_endpoint": f"{settings.API_V1_STR}/auth/login"
    }

@app.get("/health")
def health_check():
    """Endpoint de health check"""
    return {
        "status": "healthy", 
        "service": "login-only",
        "version": settings.PROJECT_VERSION
    }