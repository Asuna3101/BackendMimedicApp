from app.seeders.seed_unidades import seed_unidades
from app.seeders.seed_medicamentos import seed_medicamentos
from app.seeders.seed_healtcare import seed_healthcare
from app.seeders.seed_comidas import seed_comidas
from app.seeders.seed_categorias import seed_categorias
from app.seeders.seed_ejercicios import seed_ejercicios
from app.seeders.migrate_comidas_usuario import migrate_comidas_usuario


def run_all_seeders():
    print("Ejecutando seeders...")
    migrate_comidas_usuario()  # Ejecutar migración primero
    seed_healthcare(drop=False)
    seed_unidades()
    seed_medicamentos()
    seed_categorias()
    seed_comidas()
    seed_ejercicios()
    print("Todos los seeders completados correctamente.")

if __name__ == "__main__":
    run_all_seeders()
