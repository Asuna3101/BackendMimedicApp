from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints import auth, medicamentoxusuario, toma, unidad, healthcare, appointment_reminders
from app.core.database import engine
from app.models import base
from app.seeders.run_seeders import run_all_seeders

base.Base.metadata.create_all(bind=engine)
run_all_seeders()

app = FastAPI(
    title="MimedicApp Login API",
    version=settings.PROJECT_VERSION,
    description="API simplificada solo para login/autenticación",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["authentication"])
app.include_router(medicamentoxusuario.router,prefix=f"{settings.API_V1_STR}/medicamentos",tags=["medicamentos-usuario"],)
app.include_router(unidad.router,prefix=f"{settings.API_V1_STR}/unidades",tags=["catalogo-unidades"])
app.include_router(toma.router,prefix=f"{settings.API_V1_STR}/tomas",tags=["tomas"],)
app.include_router(healthcare.router,prefix=f"{settings.API_V1_STR}/health",tags=["healthcare"],)
app.include_router(appointment_reminders.router,prefix=f"{settings.API_V1_STR}/health/appointment-reminders",tags=["citas"],)

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