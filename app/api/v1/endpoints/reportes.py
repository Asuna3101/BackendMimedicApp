from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.api.v1.endpoints.dependencies import get_current_user
from app.core.database import get_db
from app.controllers.report_controller import ReportController
from app.controllers.user_controller import UserController
from app.schemas.reportes import CompletedTasksResponse, ReportSummary, TimelineEvent

router = APIRouter()


@router.get("/summary", response_model=ReportSummary)
def get_report_summary(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    ctl = ReportController(db)
    data = ctl.summary(current_user.id)
    return data


@router.get("/modulo", response_model=list[TimelineEvent])
def get_module_report(
    module: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    ctl = ReportController(db)
    return ctl.module_events(current_user.id, module)


@router.get("/modulo/download", response_class=PlainTextResponse)
def download_module_report(
    module: str,
    format: str = "txt",
    token: str | None = Query(None, description="Token JWT opcional"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    user = current_user
    # Si viene token por query (ej. al abrir en navegador), úsalo
    if token:
        try:
            user = UserController(db).get_current_user_from_token(token)
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    ctl = ReportController(db)
    content, mime, filename = ctl.module_download(user.id, module, format)
    from fastapi.responses import Response
    return Response(
        content=content,
        media_type=mime,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/tareas/completadas", response_model=CompletedTasksResponse)
def get_completed_tasks(
    db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    # Reusar summary y filtrar estados
    ctl = ReportController(db)
    summ = ctl.summary(current_user.id)
    timeline = summ.get("timeline", [])
    ejercicios_tasks = []
    meds_tasks = []
    citas_tasks = []
    for ev in timeline:
        t = ev.get("type")
        dt = datetime.fromisoformat(ev.get("date"))
        item = ev
        if t == "ejercicio":
            ejercicios_tasks.append(
                {"title": ev.get("title", ""), "detail": ev.get("subtitle", ""), "status": ev.get("status"), "completed_at": dt}
            )
        elif t == "toma":
            meds_tasks.append(
                {"title": ev.get("title", ""), "detail": ev.get("subtitle", ""), "status": ev.get("status"), "completed_at": dt}
            )
        elif t == "cita" and ev.get("status") and ev.get("status").lower() != "pendiente":
            citas_tasks.append(
                {"title": ev.get("title", ""), "detail": ev.get("subtitle", ""), "status": ev.get("status"), "completed_at": dt}
            )
    ejercicios_tasks.sort(key=lambda x: x["completed_at"], reverse=True)
    meds_tasks.sort(key=lambda x: x["completed_at"], reverse=True)
    citas_tasks.sort(key=lambda x: x["completed_at"], reverse=True)

    return CompletedTasksResponse(
        ejercicio=[CompletedTask(**e) for e in ejercicios_tasks],
        medicamentos=[CompletedTask(**m) for m in meds_tasks],
        citas=[CompletedTask(**c) for c in citas_tasks],
    )
