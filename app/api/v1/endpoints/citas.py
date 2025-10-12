"""
Endpoint para registrar citas
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.v1.endpoints.dependencies import get_current_user
from app.controllers.citas_controller import CitasController
from app.core.database import get_db


router = APIRouter()

@router.get("/usuario/lista")
def listar_mis_citas(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    controller = CitasController(db)
    return controller.obtener_citas_usuario(user.id)