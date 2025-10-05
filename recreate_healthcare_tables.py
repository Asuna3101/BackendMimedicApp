"""
Recrea tablas de clínicas/especialidades/doctores/disponibilidad/citas
y carga datos de ejemplo para desarrollo.
"""
import sys, os
from datetime import date, timedelta, time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from app.core.database import engine
from app.models.base import Base
from app.models.user import User
from app.auth.password_hasher import SimplePasswordHasher

from app.models.clinic import Clinic
from app.models.specialty import Specialty
from app.models.clinic_specialty import ClinicSpecialty
from app.models.doctor import Doctor
from app.models.doctor_availability import DoctorAvailability
from app.models.appointment import Appointment

def drop_tables():
    with engine.connect() as conn:
        # Orden inverso por FK
        conn.execute(text("DROP TABLE IF EXISTS citas CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS doctor_disponibilidad CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS doctores CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS clinic_especialidades CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS especialidades CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS clinicas CASCADE"))
        conn.commit()
        print("Tablas de salud eliminadas.")

def create_all():
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas.")

def seed_data(db):
    # --- Clínicas (5) ---
    clinicas = [
        Clinic(nombre="Clínica Ricardo Palma", ciudad="Lima", direccion="Av. Javier Prado Este 1066"),
        Clinic(nombre="Clínica Internacional", ciudad="Lima", direccion="Av. Alfonso Ugarte 1148"),
        Clinic(nombre="Clínica San Pablo", ciudad="Lima", direccion="Av. Guardia Civil 385"),
        Clinic(nombre="Clínica Tezza", ciudad="Lima", direccion="Av. Guardia Civil 337"),
        Clinic(nombre="Clínica Anglo Americana", ciudad="Lima", direccion="Alfredo Salazar 350"),
    ]
    db.add_all(clinicas); db.flush()

    # --- Especialidades ---
    nombres_esp = [
        "Reumatología","Mastología","Cardiología","Pediatría",
        "Ginecología","Traumatología","Dermatología","Oftalmología","Neurología"
    ]
    esp_map = {n: Specialty(nombre=n) for n in nombres_esp}
    db.add_all(esp_map.values()); db.flush()

    # --- Mapeo especialidades por clínica (no todas iguales) ---
    mapa = {
        "Clínica Ricardo Palma": ["Reumatología","Mastología","Cardiología"],
        "Clínica Internacional": ["Ginecología","Traumatología","Cardiología"],
        "Clínica San Pablo":     ["Reumatología","Pediatría","Traumatología"],
        "Clínica Tezza":         ["Dermatología","Oftalmología"],
        "Clínica Anglo Americana":["Cardiología","Neurología","Reumatología"],
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
            for i in range(1, 3):  # 2 doctores
                d = Doctor(
                    nombre=make_doctor_name(e_nom, i),
                    clinica_id=c.id,
                    especialidad_id=esp.id
                )
                doctores.append(d)
    db.add_all(doctores); db.flush()

    # --- Disponibilidad: Lunes(1) a Sábado(6), slots fijos ---
    slots = [
        (time(7,0),  time(9,0)),
        (time(11,0), time(13,0)),
        (time(15,0), time(16,0)),
        (time(17,0), time(19,0)),
    ]
    disponibilidades = []
    for d in doctores:
        for dow in range(1, 7):  # 1..6
            for (ini, fin) in slots:
                disponibilidades.append(
                    DoctorAvailability(doctor_id=d.id, day_of_week=dow, hora_inicio=ini, hora_fin=fin)
                )
    db.add_all(disponibilidades); db.flush()

    # --- Usuario de prueba (si no existe) ---
    u = db.query(User).filter(User.correo == "test@example.com").first()
    if not u:
        hasher = SimplePasswordHasher()
        u = User(
            correo="test@example.com",
            nombre="Usuario de Prueba",
            celular="1234567890",
            hashed_password=hasher.hash_password("test123"),
            is_active=True
        )
        db.add(u); db.flush()

    # --- Cita ejemplo para "bloquear" un slot (mañana 11-13 con algún doctor) ---
    manana = date.today() + timedelta(days=1)
    primer_doctor = doctores[0]
    db.add(Appointment(
        doctor_id=primer_doctor.id,
        paciente_id=u.id,
        fecha=manana,
        hora_inicio=time(11,0),
        hora_fin=time(13,0),
        estado="confirmada"
    ))
    db.commit()
    print("Seed completado.")

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
