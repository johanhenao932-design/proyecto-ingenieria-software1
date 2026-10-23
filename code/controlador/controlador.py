
from modelo.modelo import Material, Tecnico


class Controlador:
    def __init__(
        self, vista, administrador, tecnicos,
        materiales, asignaciones, devoluciones, reportes
    ):
        self.vista = vista
        self.administrador = administrador
        self.administradores = [administrador]
        self.tecnicos = tecnicos
        self.materiales = materiales
        self.asignaciones = asignaciones
        self.devoluciones = devoluciones
        self.reportes = reportes

    def iniciar(self):
        while True:
            self.vista.limpiarPantalla()
            self.vista.mostrarMensaje("INICIO DE SESIÓN")
            nombre = self.vista.pedirTexto("Usuario: ")
            contrasena = self.vista.pedirTexto("Contraseña: ")

            usuarios = self.administradores + self.tecnicos
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
        self.usuarioActual = usuario
        es_admin = usuario in self.administradores

        while True:
            self.vista.limpiarPantalla()
            opcion = self.vista.mostrarMenu(es_admin)

            try:
                if opcion == 0:
                    break

                if opcion == 1 and es_admin:
                    self.vista.mostrarMateriales(self.materiales)

                elif opcion == 1:
                    asignaciones = usuario.consultarMaterialAsignado(
                        self.asignaciones
                    )
                    self.vista.mostrarAsignaciones(asignaciones)

                elif es_admin:
                    self.opcionesAdministrador(opcion)

                else:
                    self.opcionesTecnico(opcion, usuario)

            except ValueError as error:
                self.vista.mostrarMensaje(f"Error: {error}")

            if opcion != 0:
                self.vista.esperarContinuar()

    def opcionesAdministrador(self, opcion):
        if opcion == 2:
            self.registrarMaterial()
        elif opcion == 3:
            self.crearTecnico()
        elif opcion == 4:
            self.verTecnicosActivos()
        elif opcion == 5:
            self.asignarMaterial()
        elif opcion == 6:
            tecnicosActivos = {
                tecnico.id for tecnico in self.tecnicos if tecnico.activo
            }
            asignacionesActivas = [
                asignacion for asignacion in self.asignaciones
                if asignacion.tecnico.id in tecnicosActivos
            ]
            self.vista.mostrarAsignaciones(asignacionesActivas)
        elif opcion == 7:
            self.gestionarReportes()
        elif opcion == 8:
            self.cambiarEstadoTecnico()
        elif opcion == 9:
            self.eliminarTecnico()
        elif opcion == 10:
            self.cambiarContrasena(self.usuarioActual)
        elif opcion == 11:
            self.cambiarContrasenaTecnico()
        elif opcion == 12:
            self.cambiarNombreUsuarioAdministrador()
        else:
            self.vista.mostrarMensaje("Opción inválida.")

    def crearTecnico(self):
        nombre = self.vista.pedirTexto("Nombre de usuario del técnico: ")
        contrasena = self.vista.pedirTexto("Contraseña: ")
        self.validarNuevaCuenta(nombre, contrasena)
        tecnico = Tecnico(self.siguienteIdUsuario(), nombre, contrasena)
        self.tecnicos.append(tecnico)
        self.vista.mostrarMensaje("Técnico creado correctamente.")

    def validarNuevaCuenta(self, nombre, contrasena):
        if not nombre or not contrasena:
            raise ValueError("El usuario y la contraseña son obligatorios.")
        usuarios = self.administradores + self.tecnicos
        if any(u.nombre.lower() == nombre.lower() for u in usuarios):
            raise ValueError("Ya existe una cuenta con ese usuario.")

    def siguienteIdUsuario(self):
        usuarios = self.administradores + self.tecnicos
        return max((u.id for u in usuarios), default=0) + 1

    def verTecnicosActivos(self):
        tecnicosActivos = [tecnico for tecnico in self.tecnicos if tecnico.activo]
        if not tecnicosActivos:
            self.vista.mostrarMensaje("No hay técnicos activos.")
            return
        self.vista.mostrarMensaje("TÉCNICOS ACTIVOS")
        self.vista.mostrarTecnicos(tecnicosActivos)

    def eliminarTecnico(self):
        if not self.tecnicos:
            raise ValueError("No hay cuentas de técnicos para eliminar.")

        self.vista.mostrarTecnicos(self.tecnicos)
        numero = self.vista.pedirEntero(
            "Número del técnico a eliminar (0 para volver): "
        )
        if numero == 0:
            return
        if not 1 <= numero <= len(self.tecnicos):
            raise ValueError("Número de técnico inválido.")

        tecnico = self.tecnicos[numero - 1]
        tieneMaterialPendiente = any(
            asignacion.tecnico.id == tecnico.id
            and asignacion.cantidadAsignada > asignacion.cantidadDevuelta
            for asignacion in self.asignaciones
        )
        if tieneMaterialPendiente:
            raise ValueError(
                "No se puede eliminar la cuenta: el técnico tiene material pendiente de devolución."
            )

        self.tecnicos.remove(tecnico)
        self.vista.mostrarMensaje(
            f"La cuenta del técnico {tecnico.nombre} fue eliminada."
        )
        if self.tecnicos:
            self.vista.mostrarMensaje("Técnicos que siguen registrados:")
            self.vista.mostrarTecnicos(self.tecnicos)
        else:
            self.vista.mostrarMensaje("No quedan técnicos registrados.")

    def cambiarContrasena(self, usuario):
        actual = self.vista.pedirTexto("Contraseña actual: ")
        nueva = self.vista.pedirTexto("Nueva contraseña: ")
        confirmacion = self.vista.pedirTexto("Confirma la nueva contraseña: ")
        if nueva != confirmacion:
            raise ValueError("Las contraseñas nuevas no coinciden.")
        usuario.cambiarContrasena(actual, nueva)
        self.vista.mostrarMensaje("Contraseña actualizada correctamente.")

    def cambiarContrasenaTecnico(self):
        if not self.tecnicos:
            raise ValueError("No hay cuentas de técnicos.")

        self.vista.mostrarTecnicos(self.tecnicos)
        numero = self.vista.pedirEntero(
            "Número del técnico (0 para volver): "
        )
        if numero == 0:
            return
        if not 1 <= numero <= len(self.tecnicos):
            raise ValueError("Número de técnico inválido.")

        tecnico = self.tecnicos[numero - 1]
        nueva = self.vista.pedirTexto("Nueva contraseña: ")
        confirmacion = self.vista.pedirTexto("Confirma la nueva contraseña: ")
        if nueva != confirmacion:
            raise ValueError("Las contraseñas nuevas no coinciden.")

        tecnico.restablecerContrasena(nueva)
        self.vista.mostrarMensaje(
            f"Contraseña actualizada para {tecnico.nombre}."
        )

    def cambiarNombreUsuarioAdministrador(self):
        print("\n1. Cambiar mi nombre de usuario")
        print("2. Cambiar nombre de usuario de un técnico")
        opcion = self.vista.pedirEntero("Opción (0 para volver): ")

        if opcion == 0:
            return
        if opcion == 1:
            cuenta = self.usuarioActual
        elif opcion == 2:
            if not self.tecnicos:
                raise ValueError("No hay cuentas de técnicos.")
            self.vista.mostrarTecnicos(self.tecnicos)
            numero = self.vista.pedirEntero(
                "Número del técnico (0 para volver): "
            )
            if numero == 0:
                return
            if not 1 <= numero <= len(self.tecnicos):
                raise ValueError("Número de técnico inválido.")
            cuenta = self.tecnicos[numero - 1]
        else:
            raise ValueError("Opción inválida.")

        nombreNuevo = self.vista.pedirTexto("Nuevo nombre de usuario: ")
        usuarios = self.administradores + self.tecnicos
        if not nombreNuevo:
            raise ValueError("El nombre de usuario no puede estar vacío.")
        if any(
            usuario is not cuenta
            and usuario.nombre.casefold() == nombreNuevo.casefold()
            for usuario in usuarios
        ):
            raise ValueError("Ese nombre de usuario ya está ocupado.")

        nombreAnterior = cuenta.nombre
        cuenta.cambiarNombreUsuario(nombreNuevo)
        self.vista.mostrarMensaje(
            f"Nombre de usuario actualizado: {nombreAnterior} → {cuenta.nombre}."
        )

    def gestionarReportes(self):
        if not self.reportes:
            self.vista.mostrarReportes(self.reportes)
            return

        self.vista.mostrarReportes(self.reportes)
        numero = self.vista.pedirEntero(
            "Número del reporte a actualizar (0 para volver): "
        )
        if numero == 0:
            return
        if not 1 <= numero <= len(self.reportes):
            raise ValueError("Número de reporte inválido.")

        reporte = self.reportes[numero - 1]
        reporte.diagnostico = self.vista.pedirTexto("Diagnóstico: ")
        estado = self.vista.pedirTexto(
            "Estado (Abierto, En revisión o Resuelto): "
        )
        if estado not in ("Abierto", "En revisión", "Resuelto"):
            raise ValueError("El estado indicado no es válido.")
        reporte.estado = estado
        self.vista.mostrarMensaje("Reporte actualizado correctamente.")

    def opcionesTecnico(self, opcion, tecnico):
        if opcion == 2:
            self.devolverMaterial(tecnico)

        elif opcion == 3:
            self.reportarDefecto(tecnico)

        elif opcion == 4:
            self.cambiarContrasena(tecnico)

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
