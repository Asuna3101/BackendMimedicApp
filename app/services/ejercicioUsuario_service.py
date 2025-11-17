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

        if not data.nombre.strip():
            raise ValueError("El nombre del ejercicio es obligatorio")
        
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
            "nombre": ejercicio.nombre,
            "notas": ejxuser.notas,
            "horario": ejxuser.horario,
            "duracion_min": ejxuser.duracion_min
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

    def actualizar_ejercicio_usuario(self, ejercicio_id: int, data):
        update_data = data.dict(exclude_unset=True)
        
        if "nombre" in update_data:
            ejercicio = self.ejercicio_repo.get_or_create_ejercicio(update_data.pop("nombre"))
            update_data["idEjercicio"] = ejercicio.id
        
        ejxuser = self.ejxuser_repo.update(ejercicio_id, update_data)
        if not ejxuser:
            return None
        
        ejercicio = self.ejercicio_repo.get_by_id(ejxuser.idEjercicio)
        
        return {
            "id": ejxuser.id,
            "nombre": ejercicio.nombre,
            "notas": ejxuser.notas,
            "horario": ejxuser.horario,
            "duracion_min": ejxuser.duracion_min
        }

    def eliminar_ejercicios_usuario(self, id_usuario: int, ejercicio_ids: list[int]) -> bool:
        if not ejercicio_ids:
            raise ValueError("Debe proporcionar al menos un ID para eliminar")
        
        eliminado = self.ejxuser_repo.delete(id_usuario, ejercicio_ids)
        
        if not eliminado:
            raise ValueError("No se encontraron ejercicios para eliminar (no existen o no pertenecen al usuario)")
        
        return True