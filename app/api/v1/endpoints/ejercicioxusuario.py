"""
Endpoint para ejercicio / ejercicioUsuario
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.controllers.ejercicio_controller import EjercicioController
from app.core.database import get_db
from app.schemas.ejercicio import (
    EjercicioResponse
)

router = APIRouter()

@router.get("/", response_model=list[EjercicioResponse])
def listar_ejercicios(db: Session = Depends(get_db)):
    controller = EjercicioController(db)
    return controller.listar_todos()