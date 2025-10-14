"""
Endpoints para tomas (marcar como tomada y limpieza automática)
"""
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.controllers.toma_controller import TomaController
from app.schemas.toma import TomaUpdate, TomaResponse

router = APIRouter()

@router.patch("/{toma_id}", response_model=TomaResponse)
def actualizar_toma(
    toma_id: int = Path(..., gt=0),
    data: TomaUpdate = None,
    db: Session = Depends(get_db),
):
    controller = TomaController(db)
    toma = controller.marcar_toma(toma_id, data.tomado)
    return toma
