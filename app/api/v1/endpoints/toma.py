"""
Endpoints para tomas (marcar como tomada y limpieza automática)
"""
from fastapi import APIRouter, Depends, Path, Query, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.controllers.toma_controller import TomaController
from app.schemas.toma import TomaUpdate, TomaResponse
from datetime import datetime, timezone
from typing import List

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


@router.patch("/{toma_id}/postpone")
def postpone_toma(
    toma_id: int = Path(..., gt=0),
    minutes: int = Query(..., gt=0),
    db: Session = Depends(get_db),
):
    """Pospone la toma indicada y las siguientes del mismo medicamento-usuario
    en `minutes` minutos."""
    controller = TomaController(db)
    try:
        updated = controller.postpone_tomas(toma_id, minutes)
        return {"updated": updated}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/pending", response_model=List[TomaResponse])
def get_pending_tomas(
    at: str | None = Query(None, description="ISO datetime to check (UTC). If omitted uses now UTC"),
    db: Session = Depends(get_db),
):
    """Devuelve las tomas pendientes cuya hora programada cae dentro del
    minuto indicado por `at` (UTC). Si `at` es None, se usa ahora UTC."""
    controller = TomaController(db)
    try:
        if at:
            dt = datetime.fromisoformat(at)
            # ensure timezone-aware UTC
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            else:
                dt = dt.astimezone(timezone.utc)
        else:
            dt = datetime.now(timezone.utc)

        # use repository via service factory to get pending (we'll call repo directly)
        repo = controller.service.toma_repo
        tomas = repo.get_pending_at(dt)
        return tomas
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
