"""
Recrea tablas de clínicas / especialidades / doctores
y carga datos de ejemplo para desarrollo (CATÁLOGOS SOLAMENTE).
Sin disponibilidad semanal y sin citas legacy.
"""

import sys, os
from datetime import date, time, timedelta, datetime

# permitir ejecutar el script directo
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from app.core.database import engine
from app.models.base import Base

from app.models.clinic import Clinic
from app.models.specialty import Specialty
from app.models.clinic_specialty import ClinicSpecialty
from app.models.doctor import Doctor

# from app.models.appointment_reminder import AppointmentReminder


# ----------------------------- DDL -----------------------------

def drop_tables():
    """
    Elimina tablas de salud en orden inverso por FK.
    Los nombres deben coincidir con __tablename__ de tus modelos.
    """
    with engine.connect() as conn:
        # Nuevo modelo de recordatorios (si existe)
        conn.execute(text("DROP TABLE IF EXISTS appointment_reminders CASCADE"))

        # Legacy (por si todavía existen en tu DB)
        conn.execute(text("DROP TABLE IF EXISTS citas CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS doctor_disponibilidad CASCADE"))

        # Catálogos
        conn.execute(text("DROP TABLE IF EXISTS doctores CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS clinic_especialidades CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS especialidades CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS clinicas CASCADE"))

        conn.commit()
        print("Tablas de salud eliminadas.")


def create_all():
    """
    Crea todas las tablas según los modelos actuales
    (incluye índices/constraints definidos en los modelos).
    """
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas.")


# ----------------------------- SEED -----------------------------

def seed_data(db):
    # --- Clínicas ---
    clinicas = [
        Clinic(nombre="Clínica Ricardo Palma", ciudad="Lima", direccion="Av. Javier Prado Este 1066"),
        Clinic(nombre="Clínica Internacional", ciudad="Lima", direccion="Av. Alfonso Ugarte 1148"),
        Clinic(nombre="Clínica San Pablo", ciudad="Lima", direccion="Av. Guardia Civil 385"),
        Clinic(nombre="Clínica Tezza", ciudad="Lima", direccion="Av. Guardia Civil 337"),
        Clinic(nombre="Clínica Anglo Americana", ciudad="Lima", direccion="Alfredo Salazar 350"),
    ]
    db.add_all(clinicas)
    db.flush()

    # --- Especialidades ---
    nombres_esp = [
        "Reumatología", "Mastología", "Cardiología", "Pediatría",
        "Ginecología", "Traumatología", "Dermatología", "Oftalmología", "Neurología"
    ]
    esp_map = {n: Specialty(nombre=n) for n in nombres_esp}
    db.add_all(esp_map.values())
    db.flush()

    # --- Mapeo especialidades por clínica ---
    mapa = {
        "Clínica Ricardo Palma":  ["Reumatología", "Mastología", "Cardiología"],
        "Clínica Internacional":  ["Ginecología", "Traumatología", "Cardiología"],
        "Clínica San Pablo":      ["Reumatología", "Pediatría", "Traumatología"],
        "Clínica Tezza":          ["Dermatología", "Oftalmología"],
        "Clínica Anglo Americana":["Cardiología", "Neurología", "Reumatología"],
    }

    clinica_by_name = {c.nombre: c for c in clinicas}
    for clinica_nombre, especialidades in mapa.items():
        c = clinica_by_name[clinica_nombre]
        for e_nom in especialidades:
            db.add(ClinicSpecialty(clinica_id=c.id, especialidad_id=esp_map[e_nom].id))
    db.flush()

    # --- Doctores (2 por cada especialidad de cada clínica) ---
    def make_doctor_name(base, i): return f"Dr(a). {base} {i}"

    doctores = []
    for clinica_nombre, especialidades in mapa.items():
        c = clinica_by_name[clinica_nombre]
        for e_nom in especialidades:
            esp = esp_map[e_nom]
            for i in range(1, 2 + 1):
                d = Doctor(
                    nombre=make_doctor_name(e_nom, i),
                    clinica_id=c.id,
                    especialidad_id=esp.id
                )
                doctores.append(d)
    db.add_all(doctores)
    db.flush()

    # --- (Opcional) Sembrar 1-2 recordatorios si ya tienes un user_id conocido ---
    """
    user_id_demo = 1  # reemplaza por un ID válido ya existente
    manana = date.today() + timedelta(days=1)
    starts_dt = datetime(manana.year, manana.month, manana.day, 11, 30)

    db.add(AppointmentReminder(
        user_id=user_id_demo,
        clinic_id=clinicas[0].id,
        specialty_id=esp_map["Cardiología"].id,
        doctor_id=doctores[0].id,
        starts_at=starts_dt,
        notes="Chequeo general"
    ))
    db.commit()
    print("Recordatorio(s) de ejemplo creado(s).")
    """

    db.commit()
    print("Seed de catálogos completado.")


# ----------------------------- MAIN -----------------------------

def main():
    drop_tables()
    create_all()

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
