import os
import shutil
from typing import Optional
from fastapi import HTTPException
from app.interfaces.profile_service_interface import IProfileService
from app.interfaces.user_repository_interface import IUserRepository
from app.interfaces.auth_interface import IPasswordHasher


class ProfileService(IProfileService):
    def __init__(self, user_repo: IUserRepository, hasher: IPasswordHasher, upload_dir: str = "/tmp/uploads"):
        self.user_repo = user_repo
        self.hasher = hasher
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)

    def update_photo(self, user_id: int, file_path: Optional[str], url: Optional[str]) -> str:
        if not file_path and not url:
            raise HTTPException(status_code=400, detail="Falta archivo o URL")
        photo_url = url if url else file_path
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        user.photo_url = photo_url  # requiere columna; si no existe, se ignora
        self.user_repo.db.commit()
        return photo_url

    def save_upload(self, filename: str, fileobj) -> str:
        dest = os.path.join(self.upload_dir, filename)
        with open(dest, "wb") as f:
            shutil.copyfileobj(fileobj, f)
        return dest

    def change_password(self, user_id: int, old_password: str, new_password: str) -> None:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        if not self.hasher.verify_password(old_password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")
        user.hashed_password = self.hasher.hash_password(new_password)
        self.user_repo.db.commit()

    def delete_account(self, user_id: int) -> None:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        user.is_active = False
        self.user_repo.db.commit()

    def recover_account(self, email: str) -> None:
        # Stub simple; en real se enviaría correo
        if not email:
            raise HTTPException(status_code=400, detail="Email requerido")
        return
