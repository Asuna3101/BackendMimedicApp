# app/api/v1/endpoints/__init__.py
from fastapi import APIRouter
from . import healthcare, appointment_reminders, auth  # <-- asegúrate que importas auth

api_router = APIRouter()
api_router.include_router(healthcare.router)
api_router.include_router(appointment_reminders.router)
api_router.include_router(auth.router)  # <-- monta /auth
