import smtplib
import random
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from fastapi import HTTPException
from app.interfaces.recovery_service_interface import IRecoveryService
from app.interfaces.user_repository_interface import IUserRepository
from app.interfaces.auth_interface import IPasswordHasher
from app.core.config import settings


GMAIL_USER = "mimedicapp.soporte@gmail.com"
GMAIL_PASSWORD = "fqzm nhjq jmwr mhuh"


class RecoveryService(IRecoveryService):
    def __init__(self, user_repo: IUserRepository, hasher: IPasswordHasher):
        self.user_repo = user_repo
        self.hasher = hasher

    def request_code(self, email: str) -> None:
        user = self.user_repo.get_by_email(email)
        if not user:
            # No revelamos que no existe; simplemente salimos
            return
        code = f"{random.randint(0, 9999):04d}"
        exp = datetime.now(timezone.utc) + timedelta(minutes=10)
        user.recovery_code = code
        user.recovery_expires = exp
        self.user_repo.db.commit()
        self._send_email(email, code)

    def confirm_code(self, email: str, code: str, new_password: str) -> None:
        user = self.user_repo.get_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        if not user.recovery_code or not user.recovery_expires:
            raise HTTPException(status_code=400, detail="No hay código activo")
        if user.recovery_expires < datetime.now(timezone.utc):
            raise HTTPException(status_code=400, detail="Código expirado")
        if user.recovery_code != code:
            raise HTTPException(status_code=400, detail="Código inválido")

        user.hashed_password = self.hasher.hash_password(new_password)
        user.recovery_code = None
        user.recovery_expires = None
        self.user_repo.db.commit()

    def _send_email(self, to_email: str, code: str):
        subject = "MiMedicApp · Código de recuperación"
        spaced = " ".join(list(code))
        html = f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: Arial, sans-serif; background:#f7fafc; margin:0; padding:0; }}
    .card {{
      max-width: 480px; margin:24px auto; background:#ffffff;
      border-radius:12px; padding:24px;
      box-shadow:0 8px 24px rgba(0,0,0,0.08);
      border:1px solid #e6ebf1;
    }}
    .logo {{
      width:48px; height:48px; background:#2f80ed;
      color:#fff; border-radius:12px; display:flex;
      align-items:center; justify-content:center;
      font-weight:700; font-size:20px; margin-bottom:12px;
    }}
    .title {{ color:#1f2937; font-size:20px; font-weight:700; margin:0 0 12px 0; }}
    .text {{ color:#4b5563; font-size:14px; line-height:1.6; margin:0 0 16px 0; }}
    .code {{
      display:inline-block; background:#e0f2fe; color:#0f172a;
      padding:12px 18px; border-radius:10px; letter-spacing:6px;
      font-size:22px; font-weight:700; border:1px solid #bfdbfe;
    }}
    .footer {{ color:#9ca3af; font-size:12px; margin-top:20px; }}
  </style>
</head>
<body>
  <div class="card">
    <div class="logo">M</div>
    <div class="title">Código de recuperación</div>
    <p class="text">Recibimos una solicitud para restablecer tu contraseña. Usa el siguiente código de 4 dígitos:</p>
    <div class="code">{spaced}</div>
    <p class="text">Este código expira en 10 minutos.<br>
    Si no solicitaste este cambio, puedes ignorar este correo.</p>
    <div class="footer">Equipo MiMedicApp</div>
  </div>
</body>
</html>
"""
        msg = MIMEText(html, "html", "utf-8")
        msg["Subject"] = subject
        msg["From"] = GMAIL_USER
        msg["To"] = to_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.send_message(msg)
