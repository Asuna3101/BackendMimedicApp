from app.seeders.seed_unidades import seed_unidades
from app.seeders.seed_medicamentos import seed_medicamentos


def run_all_seeders():
    print("Ejecutando seeders...")
    seed_unidades()
    seed_medicamentos()
    print("Todos los seeders completados correctamente.")

if __name__ == "__main__":
    run_all_seeders()
