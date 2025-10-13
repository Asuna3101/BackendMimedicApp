# app/api/deps.py
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.core.database import SessionLocal
from app.core.config import settings
from app.models.user import User

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(authorization: str | None = Header(default=None),
                     db: Session = Depends(get_db)) -> User:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="No autenticado",
                            headers={"WWW-Authenticate": "Bearer"})
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(status_code=401, detail="Token inválido (sin subject)")
        user_id = int(sub)
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Token inválido o expirado",
                            headers={"WWW-Authenticate": "Bearer"})

    user = db.get(User, user_id)   # en vez de db.query(User).get(...)
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user
