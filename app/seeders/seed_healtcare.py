# app/seeders/seed_healthcare.py
"""
Recrea catálogos de Salud (clínicas, especialidades, relación y doctores)
y carga datos de ejemplo. SOLO para dev. Borra tablas de salud si existen.
"""

from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from app.core.database import engine
from app.models.clinic import Clinic
from app.models.specialty import Specialty
from app.models.clinic_specialty import ClinicSpecialty
from app.models.doctor import Doctor

# Base para create_all()
from app.models import base as models_base
Base = models_base.Base

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ----------------------------- DDL -----------------------------
def _drop_healthcare_tables():
    with engine.connect() as conn:
        conn.execute(text("DROP TABLE IF EXISTS appointment_reminders CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS citas CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS doctor_disponibilidad CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS doctores CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS clinic_especialidades CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS especialidades CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS clinicas CASCADE"))
        conn.commit()
    print("🧹 Tablas de salud eliminadas.")


def _create_all_models():
    Base.metadata.create_all(bind=engine)
    print("🏗️ Tablas creadas (según modelos).")


# ----------------------------- SEED -----------------------------
def _seed_catalogs(db):
    # Clínicas
    clinicas_data = [
        dict(nombre="Clínica Ricardo Palma", ciudad="Lima", direccion="Av. Javier Prado Este 1066"),
        dict(nombre="Clínica Internacional", ciudad="Lima", direccion="Av. Alfonso Ugarte 1148"),
        dict(nombre="Clínica San Pablo", ciudad="Lima", direccion="Av. Guardia Civil 385"),
        dict(nombre="Clínica Tezza", ciudad="Lima", direccion="Av. Guardia Civil 337"),
        dict(nombre="Clínica Anglo Americana", ciudad="Lima", direccion="Alfredo Salazar 350"),
    ]
    clinicas = []
    for c in clinicas_data:
        obj = db.query(Clinic).filter(Clinic.nombre == c["nombre"]).first()
        if not obj:
            obj = Clinic(**c)
            db.add(obj)
            db.flush()
            print(f"🏥 Clínica insertada: {obj.nombre}")
        clinicas.append(obj)

    # Especialidades
    nombres_esp = [
        "Reumatología", "Mastología", "Cardiología", "Pediatría",
        "Ginecología", "Traumatología", "Dermatología", "Oftalmología", "Neurología"
    ]
    esp_map = {}
    for n in nombres_esp:
        esp = db.query(Specialty).filter(Specialty.nombre == n).first()
        if not esp:
            esp = Specialty(nombre=n)
            db.add(esp)
            db.flush()
            print(f"📚 Especialidad insertada: {esp.nombre}")
        esp_map[n] = esp

    # Mapeo clínica–especialidad
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
            existe = (
                db.query(ClinicSpecialty)
                .filter(
                    ClinicSpecialty.clinica_id == c.id,
                    ClinicSpecialty.especialidad_id == esp_map[e_nom].id,
                )
                .first()
            )
            if not existe:
                db.add(ClinicSpecialty(clinica_id=c.id, especialidad_id=esp_map[e_nom].id))
                print(f"🔗 Vinculado: {clinica_nombre} ↔ {e_nom}")
    db.flush()

    # Doctores (2 por cada relación clínica–especialidad)
    def make_doctor_name(base, i): return f"Dr(a). {base} {i}"
    for clinica_nombre, especialidades in mapa.items():
        c = clinica_by_name[clinica_nombre]
        for e_nom in especialidades:
            esp = esp_map[e_nom]
            for i in range(1, 3):
                nombre = make_doctor_name(e_nom, i)
                existe = (
                    db.query(Doctor)
                    .filter(
                        Doctor.nombre == nombre,
                        Doctor.clinica_id == c.id,
                        Doctor.especialidad_id == esp.id,
                    )
                    .first()
                )
                if not existe:
                    db.add(Doctor(nombre=nombre, clinica_id=c.id, especialidad_id=esp.id))
                    print(f"🩺 Doctor insertado: {nombre} ({clinica_nombre} / {e_nom})")

    db.commit()
    print("✅ Seed de catálogos de salud completado.")


def recreate_and_seed_healthcare():
    """Borra SOLO tablas de salud, recrea y carga seed de catálogos."""
    _drop_healthcare_tables()
    _create_all_models()
    db = SessionLocal()
    try:
        _seed_catalogs(db)
    finally:
        db.close()


if __name__ == "__main__":
    recreate_and_seed_healthcare()
