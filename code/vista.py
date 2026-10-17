
class Vista:
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
        print("\n========== GESTIÓN DE MATERIAL ==========")
        print("1. Consultar inventario")

        if es_admin:
            print("2. Registrar o ingresar material")
            print("3. Asignar material a un técnico")
            print("4. Ver historial de asignaciones")
            print("5. Activar o desactivar técnico")
        else:
            print("2. Consultar mis materiales")
            print("3. Devolver material")
            print("4. Reportar material defectuoso")

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
                f"Material: {r.material.nombre} | "
                f"Fecha: {r.fecha} | Descripción: {r.descripcion} | "
                f"Diagnóstico: {r.diagnostico} | Estado: {r.estado}"
            )
