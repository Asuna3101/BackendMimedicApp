from app.seeders.seed_unidades import seed_unidades
from app.seeders.seed_medicamentos import seed_medicamentos
from app.seeders.seed_healtcare import seed_healthcare
from app.seeders.seed_ejercicios import seed_ejercicios


def run_all_seeders():
    print("Ejecutando seeders...")
    seed_healthcare(drop=False)
    seed_unidades()
    seed_medicamentos()
    seed_ejercicios()
    print("Todos los seeders completados correctamente.")

if __name__ == "__main__":
    run_all_seeders()
