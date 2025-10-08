"""
Endpoint para registrar medicamentos asociados a un usuario
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.controllers.medicamentoUsuario_controller import MedicamentoUsuarioController
from app.schemas.medicamentoUsuario import (
    MedicamentoUsuarioCreate,
)

router = APIRouter()

@router.post("/usuario/registrar")
def registrar_medicamento_usuario(
    data: MedicamentoUsuarioCreate,
    db: Session = Depends(get_db),
    # ⚠️ En producción, obtén el id_usuario desde el JWT
    id_usuario: int = 1,
):
    controller = MedicamentoUsuarioController(db)
    return controller.registrar_medicamento_usuario(id_usuario, data)

@router.get("/usuario/{id_usuario}")
def listar_medicamentos_usuario(
    id_usuario: int,
    db: Session = Depends(get_db)
):
    controller = MedicamentoUsuarioController(db)
    return controller.obtener_medicamentos_usuario(id_usuario)
