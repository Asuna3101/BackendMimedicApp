from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, PlainTextResponse

from app.core.config import settings
from app.core.database import engine, Base
import app.models as models
from app.api.v1.endpoints import api_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MimedicApp API",
    version=settings.PROJECT_VERSION,
    description="API de autenticación y agenda médica",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# CORS “normal”
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1|192\.168\.\d+\.\d+)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
)

# Middleware que RESPONDE al preflight (OPTIONS) con PNA habilitado
class PreflightPNAMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Solo intercepta preflight
        if request.method == "OPTIONS":
            origin = request.headers.get("origin", "*")
            req_headers = request.headers.get("access-control-request-headers", "*")
            req_method  = request.headers.get("access-control-request-method", "*")

            headers = {
                "Access-Control-Allow-Origin": origin,
                "Vary": "Origin",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Methods": req_method or "*",
                "Access-Control-Allow-Headers": req_headers or "*",
                # ⬇️ lo que Chrome pide para redes privadas (192.168.x.x)
                "Access-Control-Allow-Private-Network": "true",
                "Access-Control-Max-Age": "600",
            }
            # 204 sin cuerpo para preflight
            return Response(status_code=204, headers=headers)

        # Resto de requests siguen su flujo
        response = await call_next(request)
        return response

# IMPORTANTE: este middleware debe ir DESPUÉS de CORS para envolverlo “por fuera”
app.add_middleware(PreflightPNAMiddleware)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "message": "MimedicApp API",
        "version": settings.PROJECT_VERSION,
        "docs": "/docs",
        "login_endpoint": f"{settings.API_V1_STR}/auth/login",
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "api", "version": settings.PROJECT_VERSION}
