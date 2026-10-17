
import os


class Vista:
    def limpiarPantalla(self):
        os.system("cls" if os.name == "nt" else "clear")

    def esperarContinuar(self):
        input("\nPresiona Enter para volver al menú...")

    def mostrarMensaje(self, mensaje):
        print(f"\n{mensaje}")

    def pedirTexto(self, mensaje):
        return input(mensaje).strip()

    def pedirEntero(self, mensaje):
        while True:
            try:
                return int(input(mensaje))
            except ValueError:
                print("Error: ingresa un número entero.")

    def mostrarMenu(self, es_admin):
        if es_admin:
            print("\n--- MENÚ ADMINISTRADOR ---")
            print("1. Ver inventario")
            print("2. Registrar material")
            print("3. Crear técnico")
            print("4. Ver técnicos activos")
            print("5. Asignar material")
            print("6. Ver asignaciones")
            print("7. Ver/actualizar reportes de daño")
            print("8. Activar o desactivar técnico")
            print("9. Eliminar cuenta de técnico")
            print("10. Cambiar mi contraseña")
            print("11. Cambiar contraseña de un técnico")
            print("12. Cambiar nombre de usuario")
        else:
            print("\n--- MENÚ TÉCNICO ---")
            print("1. Consultar mis materiales")
            print("2. Devolver material")
            print("3. Reportar material defectuoso")
            print("4. Cambiar mi contraseña")

        print("0. Cerrar sesión")
        return self.pedirEntero("Selecciona una opción: ")

    def mostrarMateriales(self, materiales):
        print("\n--- INVENTARIO ---")

        if not materiales:
            print("No hay materiales registrados.")
            return

        for m in materiales:
            print(
                f"Código: {m.codigo} | Nombre: {m.nombre} | "
                f"Stock: {m.stock} | Mínimo: {m.stockMinimo} | "
                f"Estado: {m.estado}"
            )

    def mostrarAsignaciones(self, asignaciones):
        print("\n--- ASIGNACIONES ---")

        if not asignaciones:
            print("No hay asignaciones para mostrar.")
            return

        for i, a in enumerate(asignaciones, start=1):
            pendiente = a.cantidadAsignada - a.cantidadDevuelta
            print(
                f"{i}. Técnico: {a.tecnico.nombre} | "
                f"Material: {a.material.nombre} ({a.material.codigo}) | "
                f"Asignado: {a.cantidadAsignada} | "
                f"Devuelto: {a.cantidadDevuelta} | "
                f"Pendiente: {pendiente} | Estado: {a.estado} | "
                f"Límite: {a.fechaLimiteDevolucion}"
            )

    def mostrarTecnicos(self, tecnicos):
        for i, tecnico in enumerate(tecnicos, start=1):
            estado = "Activo" if tecnico.activo else "Inactivo"
            print(f"{i}. {tecnico.nombre} - {estado}")

    def mostrarReportes(self, reportes):
        print("\n--- REPORTES DE DEFECTOS ---")

        if not reportes:
            print("No hay reportes registrados.")
            return

        for r in reportes:
            print(
                f"{reportes.index(r) + 1}. Material: {r.material.nombre} | "
                f"Fecha: {r.fecha} | Descripción: {r.descripcion} | "
                f"Diagnóstico: {r.diagnostico} | Estado: {r.estado}"
            )
