
from modelo import Administrador, Tecnico, Material
from vista import Vista
from controlador import Controlador


def main():
    # Crear el administrador.
    administrador = Administrador(
        1, "admin", "admin123"
    )

    # Crear técnicos de prueba.
    tecnicos = [
        Tecnico(2, "tecnico1", "tec123"),
        Tecnico(3, "tecnico2", "tec456")
    ]

    # Crear inventario inicial.
    materiales = [
        Material("M001", "Taladro", 10, 2),
        Material("M002", "Casco de seguridad", 20, 5),
        Material("M003", "Guantes", 30, 10)
    ]

    for material in materiales:
        material.actualizarEstado()

    # Crear listas para guardar las operaciones durante la ejecución.
    asignaciones = []
    devoluciones = []
    reportes = []

    # Crear la vista.
    vista = Vista()

    # Crear el controlador y conectar todos los componentes.
    controlador = Controlador(
        vista,
        administrador,
        tecnicos,
        materiales,
        asignaciones,
        devoluciones,
        reportes
    )

    # Iniciar el programa.
    controlador.iniciar()


if __name__ == "__main__":
    main()
