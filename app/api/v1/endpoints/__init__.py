# app/api/v1/endpoints/__init__.py
from fastapi import APIRouter

from . import healthcare as healthcare_endpoints
from . import appointment_reminders as reminders_endpoints
from . import auth as auth_endpoints

api_router = APIRouter()
api_router.include_router(healthcare_endpoints.router)        # /api/v1/health/...
api_router.include_router(reminders_endpoints.router)         # /api/v1/health/appointment-reminders/...
api_router.include_router(auth_endpoints.router)              # /api/v1/auth/...
