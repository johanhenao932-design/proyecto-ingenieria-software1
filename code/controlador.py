
from modelo import Material


class Controlador:
    def __init__(
        self, vista, administrador, tecnicos,
        materiales, asignaciones, devoluciones, reportes
    ):
        self.vista = vista
        self.administrador = administrador
        self.tecnicos = tecnicos
        self.materiales = materiales
        self.asignaciones = asignaciones
        self.devoluciones = devoluciones
        self.reportes = reportes

    def iniciar(self):
        while True:
            self.vista.mostrarMensaje("INICIO DE SESIÓN")
            nombre = self.vista.pedirTexto("Usuario: ")
            contrasena = self.vista.pedirTexto("Contraseña: ")

            usuarios = [self.administrador] + self.tecnicos
            usuario = next(
                (u for u in usuarios if u.nombre == nombre), None
            )

            if usuario is None or not usuario.iniciarSesion(contrasena):
                self.vista.mostrarMensaje(
                    "Credenciales incorrectas o usuario inactivo."
                )
                continuar = self.vista.pedirTexto(
                    "¿Intentar de nuevo? (s/n): "
                ).lower()

                if continuar != "s":
                    break
                continue

            self.vista.mostrarMensaje(
                f"Bienvenido, {usuario.nombre}"
            )
            self.menuUsuario(usuario)
            usuario.cerrarSesion()
            self.vista.mostrarMensaje("Sesión cerrada.")

    def menuUsuario(self, usuario):
        es_admin = usuario.id == self.administrador.id

        while True:
            opcion = self.vista.mostrarMenu(es_admin)

            try:
                if opcion == 0:
                    break

                if opcion == 1:
                    self.vista.mostrarMateriales(self.materiales)

                elif es_admin:
                    self.opcionesAdministrador(opcion)

                else:
                    self.opcionesTecnico(opcion, usuario)

            except ValueError as error:
                self.vista.mostrarMensaje(f"Error: {error}")

    def opcionesAdministrador(self, opcion):
        if opcion == 2:
            self.registrarMaterial()
        elif opcion == 3:
            self.asignarMaterial()
        elif opcion == 4:
            self.vista.mostrarAsignaciones(self.asignaciones)
            self.vista.mostrarReportes(self.reportes)
        elif opcion == 5:
            self.cambiarEstadoTecnico()
        else:
            self.vista.mostrarMensaje("Opción inválida.")

    def opcionesTecnico(self, opcion, tecnico):
        if opcion == 2:
            asignaciones = tecnico.consultarMaterialAsignado(
                self.asignaciones
            )
            self.vista.mostrarAsignaciones(asignaciones)

        elif opcion == 3:
            self.devolverMaterial(tecnico)

        elif opcion == 4:
            self.reportarDefecto(tecnico)

        else:
            self.vista.mostrarMensaje("Opción inválida.")

    def registrarMaterial(self):
        codigo = self.vista.pedirTexto("Código: ")
        nombre = self.vista.pedirTexto("Nombre: ")
        stock = self.vista.pedirEntero("Cantidad a ingresar: ")
        minimo = self.vista.pedirEntero("Stock mínimo: ")

        if not codigo or not nombre:
            raise ValueError("El código y el nombre son obligatorios.")

        if stock <= 0 or minimo < 0:
            raise ValueError(
                "La cantidad debe ser positiva y el mínimo no negativo."
            )

        material = Material(codigo, nombre, stock, minimo)
        self.administrador.ingresarMaterial(material, self.materiales)
        self.vista.mostrarMensaje("Material ingresado correctamente.")

    def asignarMaterial(self):
        if not self.materiales:
            raise ValueError("No hay materiales registrados.")

        if not self.tecnicos:
            raise ValueError("No hay técnicos registrados.")

        print("\n--- TÉCNICOS ---")
        self.vista.mostrarTecnicos(self.tecnicos)
        numero = self.vista.pedirEntero("Número del técnico: ")

        if not 1 <= numero <= len(self.tecnicos):
            raise ValueError("Número de técnico inválido.")

        tecnico = self.tecnicos[numero - 1]

        print("\n--- MATERIALES ---")
        self.vista.mostrarMateriales(self.materiales)
        codigo = self.vista.pedirTexto("Código del material: ")

        material = next(
            (m for m in self.materiales if m.codigo == codigo), None
        )

        if material is None:
            raise ValueError("Material no encontrado.")

        cantidad = self.vista.pedirEntero("Cantidad a asignar: ")

        asignacion = self.administrador.asignarMaterial(
            tecnico, material, cantidad, self.asignaciones
        )

        self.vista.mostrarMensaje(
            f"Asignación registrada. Fecha límite: "
            f"{asignacion.fechaLimiteDevolucion}"
        )

    def devolverMaterial(self, tecnico):
        pendientes = [
            a for a in self.asignaciones
            if a.tecnico.id == tecnico.id
            and a.cantidadAsignada > a.cantidadDevuelta
        ]

        if not pendientes:
            self.vista.mostrarMensaje("No tienes devoluciones pendientes.")
            return

        self.vista.mostrarAsignaciones(pendientes)
        codigo = self.vista.pedirTexto("Código del material: ")

        asignacion = next(
            (a for a in pendientes if a.material.codigo == codigo), None
        )

        if asignacion is None:
            raise ValueError("No tienes ese material asignado.")

        cantidad = self.vista.pedirEntero("Cantidad a devolver: ")
        defectuoso = self.vista.pedirTexto(
            "¿Está defectuoso? (s/n): "
        ).lower() == "s"

        devolucion = tecnico.devolverMaterial(
            asignacion, cantidad, self.devoluciones, defectuoso
        )

        if defectuoso:
            descripcion = self.vista.pedirTexto(
                "Describe el defecto: "
            )
            tecnico.devolverMaterialDefectuoso(
                asignacion.material,
                descripcion,
                self.reportes
            )

        self.vista.mostrarMensaje(
            f"Devolución registrada. Estado: {devolucion.estado}"
        )

    def reportarDefecto(self, tecnico):
        asignaciones = [
            a for a in self.asignaciones
            if a.tecnico.id == tecnico.id
        ]

        if not asignaciones:
            raise ValueError(
                "No tienes asignaciones para reportar."
            )

        codigo = self.vista.pedirTexto("Código del material: ")
        material = next(
            (a.material for a in asignaciones
             if a.material.codigo == codigo), None
        )

        if material is None:
            raise ValueError(
                "El material no pertenece a tus asignaciones."
            )

        descripcion = self.vista.pedirTexto("Describe el defecto: ")
        reporte = tecnico.devolverMaterialDefectuoso(
            material, descripcion, self.reportes
        )
        self.vista.mostrarMensaje(
            f"Reporte registrado. Estado: {reporte.estado}"
        )

    def cambiarEstadoTecnico(self):
        if not self.tecnicos:
            raise ValueError("No hay técnicos registrados.")

        self.vista.mostrarTecnicos(self.tecnicos)
        numero = self.vista.pedirEntero("Número del técnico: ")

        if not 1 <= numero <= len(self.tecnicos):
            raise ValueError("Número de técnico inválido.")

        tecnico = self.tecnicos[numero - 1]
        nuevo_estado = not tecnico.activo

        self.administrador.gestionarCuentaTecnico(
            tecnico, nuevo_estado
        )

        estado = "activo" if nuevo_estado else "inactivo"
        self.vista.mostrarMensaje(
            f"El técnico {tecnico.nombre} ahora está {estado}."
        )
