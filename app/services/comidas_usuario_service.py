"""
Servicio para la lógica de comidas_usuario
"""
from app.repositories.comidas_usuario_repo import ComidaUsuarioRepository
from app.models.comidas_usuario import ComidaUsuario


class ComidasUsuarioService:
    def __init__(self, repo: ComidaUsuarioRepository):
        self.repo = repo

    def create_for_user(self, comida_id: int, usuario_id: int, categoria_id: int | None = None) -> ComidaUsuario:
        return self.repo.create(comida_id, usuario_id, categoria_id)

    def list_for_user(self, usuario_id: int):
        return self.repo.get_by_user(usuario_id)

    def delete(self, id: int) -> bool:
        return self.repo.delete(id)
