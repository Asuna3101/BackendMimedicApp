"""
Endpoint para registrar medicamentos 
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.controllers.medicamento_controller import MedicamentoController
from app.core.database import get_db
from app.controllers.medicamentoUsuario_controller import MedicamentoUsuarioController
from app.api.v1.endpoints.dependencies import get_current_user 
from app.schemas.medicamentoUsuario import (
    MedicamentoUsuarioCreate,
)

router = APIRouter()

@router.get("/")
def listar_medicamentos(db: Session = Depends(get_db)):
    controller = MedicamentoController(db)
    return controller.listar_todos()

@router.post("/usuario/registrar")
def registrar_medicamento_usuario(
    data: MedicamentoUsuarioCreate,
    db: Session = Depends(get_db),
    # ⚠️ En producción, obtén el id_usuario desde el JWT
    user=Depends(get_current_user), 
):
    controller = MedicamentoUsuarioController(db)
    return controller.registrar_medicamento_usuario(user.id, data)

@router.get("/usuario/lista")
def listar_mis_medicamentos(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)  # ✅ obtiene el usuario desde el token
):
    controller = MedicamentoUsuarioController(db)
    return controller.obtener_medicamentos_usuario(user.id)
