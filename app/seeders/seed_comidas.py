from sqlalchemy.orm import sessionmaker
from app.core.database import engine
from app.models.comidas import Alimento

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_comidas():
    db = SessionLocal()
    comidas = [
        ("Manzana", "Fruta fresca, buena fuente de fibra"),
        ("Plátano", "Fuente de potasio"),
        ("Papas fritas", "Alto en grasas y sal"),
        ("Ensalada verde", "Lechuga, tomate, pepino"),
        ("Refresco azucarado", "Bebida con alto contenido de azúcar"),
    ]
    for nombre, detalles in comidas:
        existe = db.query(Alimento).filter(Alimento.nombre == nombre).first()
        if not existe:
            db.add(Alimento(nombre=nombre, detalles=detalles))
            print(f"Insertado alimento: {nombre}")
    db.commit()
    db.close()
    print("Seed de comidas completado.")


if __name__ == "__main__":
    seed_comidas()
