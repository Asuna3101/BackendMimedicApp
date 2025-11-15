from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.factories.service_factory import ServiceFactory


class EjercicioUsuarioController:

    def __init__(self, db: Session):
        ejxuser_repo = ServiceFactory.create_ejercicio_usuario_repository(db)
        ejercicio_repo = ServiceFactory.create_ejercicio_repository(db)
        self.service = ServiceFactory.create_ejercicio_usuario_service(ejxuser_repo, ejercicio_repo)

    def registrar(self, id_usuario: int, data):
        try:
            return self.service.registrar_ejercicio_usuario(id_usuario, data)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al registrar ejercicio: {str(e)}"
            )

    def listar(self, id_usuario: int):
        return self.service.obtener_ejercicios_usuario(id_usuario)

    def actualizar(self, ejercicio_id: int, data):
        updated = self.service.actualizar_ejercicio_usuario(ejercicio_id, data)
        if not updated:
            raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
        return updated

    def eliminar(self, ejercicio_id: int):
        if not self.service.eliminar_ejercicio_usuario(ejercicio_id):
            raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
        return {"message": "Ejercicio eliminado correctamente"}