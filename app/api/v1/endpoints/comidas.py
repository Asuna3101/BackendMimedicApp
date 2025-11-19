from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.controllers.comida_controller import ComidaController
from app.schemas.comida import ComidaOut, ComidaCreate
from app.api.v1.endpoints.dependencies import get_current_user
from app.controllers.comidas_usuario_controller import ComidaUsuarioController

router = APIRouter()


@router.get("/", response_model=list[ComidaOut])
def listar_comidas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    controller = ComidaController(db)
    return controller.listar_todas(skip=skip, limit=limit)


@router.get("/{id}", response_model=ComidaOut)
def obtener_comida(id: int, db: Session = Depends(get_db)):
    controller = ComidaController(db)
    return controller.obtener_por_id(id)


@router.post("/", response_model=ComidaOut, status_code=status.HTTP_201_CREATED)
def crear_comida(
    payload: ComidaCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    """Crear/usar un alimento del catálogo y asociarlo al usuario autenticado.
    - Si el alimento no existe en el catálogo se crea.
    - Se crea una fila en `comidas_usuario` apuntando al alimento y al usuario.
    """
    comida_ctrl = ComidaController(db)
    # Crear o obtener item del catálogo
    alm = comida_ctrl.obtener_o_crear(payload.nombre, detalles=payload.detalles, recomendable=payload.recomendable)

    # Crear asociación usuario <-> comida
    cu_ctrl = ComidaUsuarioController(db)
    cu = cu_ctrl.create_for_user(alm.id, user.id, categoria_id=payload.idCategoria)

    # Devolver el item del catálogo para compatibilidad con cliente
    return alm


@router.put("/{id}", response_model=ComidaOut)
def actualizar_comida(id: int, payload: ComidaCreate, db: Session = Depends(get_db)):
    controller = ComidaController(db)
    return controller.actualizar(id, nombre=payload.nombre, detalles=payload.detalles, recomendable=payload.recomendable)


@router.delete("/{id}")
def eliminar_comida(id: int, db: Session = Depends(get_db)):
    controller = ComidaController(db)
    return controller.eliminar(id)


@router.get("/sections", response_model=dict)
def listar_por_secciones(db: Session = Depends(get_db), user = Depends(get_current_user)):
    """Devuelve dos listas: recomendables y no_recomendables"""
    # Return per-user sections (requires authentication)
    user = Depends(get_current_user)
    cu_ctrl = ComidaUsuarioController(db)
    items = cu_ctrl.list_for_user(user.id)
    recomendables = []
    no_recomendables = []
    for cu in items:
        # cu.categoria may be None for legacy entries
        nombre_cat = (cu.categoria.nombre if getattr(cu, 'categoria', None) else None)
        if nombre_cat and nombre_cat.lower().startswith('rec'):
            recomendables.append(cu.comida)
        else:
            no_recomendables.append(cu.comida)
    return {"recomendables": recomendables, "no_recomendables": no_recomendables}


@router.get("/filter", response_model=list[ComidaOut])
def listar_filtrado(recomendable: int | None = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    controller = ComidaController(db)
    # Filtering by 'recomendable' is now a user-scoped property. Return catalog when not provided.
    if recomendable is None:
        return controller.listar_todas(skip=skip, limit=limit)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Filtro 'recomendable' ahora es por usuario; use endpoint autenticado para filtrar")
