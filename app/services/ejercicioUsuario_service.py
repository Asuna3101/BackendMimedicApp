"""
Servicio para registrar ejercicios asociados a un usuario
"""
from app.interfaces.ejercicio_repository_interface import IEjercicioRepository
from app.interfaces.ejercicio_usuario_repository_interface import IEjercicioUsuarioRepository
from app.interfaces.ejercicio_usuario_service_interface import IEjercicioUsuarioService


class EjercicioUsuarioService(IEjercicioUsuarioService):

    def __init__(
            self, 
            ejxuser_repo: IEjercicioUsuarioRepository,
            ejercicio_repo: IEjercicioRepository
    ):
        self.ejxuser_repo = ejxuser_repo
        self.ejercicio_repo = ejercicio_repo

    def registrar_ejercicio_usuario(self, id_usuario: int, data):
        ejercicio = self.ejercicio_repo.get_or_create_ejercicio(data.nombre)

        # Validaciones básicas
        if not data.nombre.strip():
            raise ValueError("El nombre del ejercicio es obligatorio")
        
        # Crear data final
        ejxuser_data = {
            "idUsuario": id_usuario,
            "idEjercicio": ejercicio.id,      
            "notas": data.notas,
            "horario": data.horario,
            "duracion_min": data.duracion_min
        }

        ejxuser = self.ejxuser_repo.create(ejxuser_data)

        return {
            "id": ejxuser.id,
            "nombre": data.nombre,
            "message": "Ejercicio guardado correctamente"
        }

    def obtener_ejercicios_usuario(self, id_usuario: int):
        rows = self.ejxuser_repo.get_by_usuario(id_usuario)

        return [
            {
                "id": exu.id,
                "nombre": e.nombre,
                "notas": exu.notas,
                "horario": exu.horario,
                "duracion_min": exu.duracion_min,
            }
            for exu, e in rows
        ]

# probablamente para actualizar se tenga que validar que el nombre del ejercicio sea nuevo o ya este creado, con el get_or_create del ejercicio
    def actualizar_ejercicio_usuario(self, ejercicio_id: int, data):
        ejxuser = self.ejxuser_repo.update(ejercicio_id, data.dict(exclude_unset=True))
        if not ejxuser:
            return None
        
        return {
            "id": ejxuser.id,
            "message": "Ejercicio actualizado correctamente"
        }

    def eliminar_ejercicio_usuario(self, ejercicio_id: int) -> bool:
        return self.ejxuser_repo.delete(ejercicio_id)