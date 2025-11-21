from app.factories.service_factory import ServiceFactory
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


class ComidaUsuarioController:
    def __init__(self, db: Session):
        comida_repo = ServiceFactory.create_comida_repository(db)
        cu_repo = ServiceFactory.create_comida_usuario_repository(db)
        self.comida_service = ServiceFactory.create_comida_service(comida_repo)
        self.service = ServiceFactory.create_comida_usuario_service(cu_repo)

    def registrar(self, id_usuario: int, data):
        """Registra una comida para el usuario (crea en catálogo si no existe)"""
        try:
            # 1. Obtener o crear la comida en el catálogo
            nombre = data.nombre
            detalles = data.detalles if hasattr(data, 'detalles') else ""
            
            comida = self.comida_service.obtener_o_crear(nombre, detalles)
            
            # 2. Crear asociación usuario-comida con categoría
            categoria_id = data.idCategoria if hasattr(data, 'idCategoria') else None
            return self.service.create_for_user(comida.id, id_usuario, categoria_id)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al registrar comida: {str(e)}"
            )

    def listar(self, id_usuario: int):
        """Lista todas las comidas del usuario"""
        try:
            return self.service.list_for_user(id_usuario)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener comidas del usuario: {str(e)}"
            )

    def delete(self, id: int):
        try:
            ok = self.service.delete(id)
            if not ok:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro no encontrado")
            return {"deleted": True}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def eliminar(self, id_usuario: int, comida_ids: list[int]):
        """Elimina múltiples comidas del usuario"""
        try:
            ok = self.service.delete_multiple(comida_ids)
            if not ok:
                raise ValueError("No se pudieron eliminar las comidas")
            return {
                "success": True,
                "message": "Comidas eliminadas correctamente"
            }
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al eliminar comidas: {str(e)}"
            )
