
from datetime import date, timedelta


class Usuario:
    def __init__(self, id, nombre, contrasena):
        self.id = id
        self.nombre = nombre
        self.contrasena = contrasena
        self.activo = True

    def iniciarSesion(self, contrasena):
        return self.activo and self.contrasena == contrasena

    def cerrarSesion(self):
        return True

    def cambiarContrasena(self, contrasenaActual, contrasenaNueva):
        if not self.iniciarSesion(contrasenaActual):
            raise ValueError("La contraseña actual es incorrecta.")

        if not contrasenaNueva.strip():
            raise ValueError("La nueva contraseña no puede estar vacía.")

        self.contrasena = contrasenaNueva

    def restablecerContrasena(self, contrasenaNueva):
        if not contrasenaNueva.strip():
            raise ValueError("La nueva contraseña no puede estar vacía.")

        self.contrasena = contrasenaNueva

    def cambiarNombreUsuario(self, nombreNuevo):
        if not nombreNuevo.strip():
            raise ValueError("El nombre de usuario no puede estar vacío.")

        self.nombre = nombreNuevo.strip()

    def verMaterialAsignado(self, asignaciones):
        return [
            a for a in asignaciones
            if a.tecnico.id == self.id
            and a.cantidadAsignada > a.cantidadDevuelta
        ]


class Material:
    def __init__(self, codigo, nombre, stock, stockMinimo):
        self.codigo = codigo
        self.nombre = nombre
        self.stock = stock
        self.stockMinimo = stockMinimo
        self.estado = "Disponible"

    def actualizarEstado(self):
        if self.stock == 0:
            self.estado = "Agotado"
        elif self.stock <= self.stockMinimo:
            self.estado = "Stock bajo"
        else:
            self.estado = "Disponible"


class Asignacion:
    def __init__(self, tecnico, material, cantidad):
        self.tecnico = tecnico
        self.material = material
        self.fecha = date.today()
        self.fechaLimiteDevolucion = date.today() + timedelta(days=7)
        self.cantidadAsignada = cantidad
        self.cantidadDevuelta = 0
        self.estado = "Activa"


class Devolucion:
    def __init__(self, asignacion, cantidad, defectuoso=False):
        self.asignacion = asignacion
        self.fecha = date.today()
        self.cantidad = cantidad
        self.estado = "Pendiente de revisión" if defectuoso else "Recibida"
        self.defectuoso = defectuoso


class ReporteDefecto:
    def __init__(self, material, descripcion, fotos=None):
        self.material = material
        self.fecha = date.today()
        self.descripcion = descripcion
        self.fotos = fotos if fotos is not None else []
        self.diagnostico = "Pendiente"
        self.estado = "Abierto"


class Administrador(Usuario):
    def ingresarMaterial(self, material, materiales):
        for existente in materiales:
            if existente.codigo == material.codigo:
                existente.stock += material.stock
                existente.actualizarEstado()
                return existente

        material.actualizarEstado()
        materiales.append(material)
        return material

    def asignarMaterial(self, tecnico, material, cantidad, asignaciones):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        if not tecnico.activo:
            raise ValueError("El técnico está inactivo.")

        if material.stock < cantidad:
            raise ValueError("No hay suficiente stock.")

        material.stock -= cantidad
        material.actualizarEstado()

        asignacion = Asignacion(tecnico, material, cantidad)
        asignaciones.append(asignacion)
        return asignacion

    def verMaterialGeneral(self, materiales):
        return materiales

    def verHistorial(self, asignaciones):
        return asignaciones

    def gestionarCuentaTecnico(self, tecnico, activo):
        tecnico.activo = activo

    def recibirNotificacion(self, mensaje):
        return mensaje


class Tecnico(Usuario):
    def consultarMaterialAsignado(self, asignaciones):
        return self.verMaterialAsignado(asignaciones)

    def recibirMaterial(self, asignacion):
        return asignacion.estado == "Activa"

    def devolverMaterial(
        self, asignacion, cantidad, devoluciones, defectuoso=False
    ):
        pendiente = (
            asignacion.cantidadAsignada - asignacion.cantidadDevuelta
        )

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        if cantidad > pendiente:
            raise ValueError("La cantidad supera la pendiente.")

        asignacion.cantidadDevuelta += cantidad

        # Solo los materiales en buen estado vuelven al inventario.
        if not defectuoso:
            asignacion.material.stock += cantidad
            asignacion.material.actualizarEstado()

        devolucion = Devolucion(asignacion, cantidad, defectuoso)
        devoluciones.append(devolucion)

        if asignacion.cantidadDevuelta == asignacion.cantidadAsignada:
            asignacion.estado = "Devuelta"

        return devolucion

    def devolverMaterialDefectuoso(
        self, material, descripcion, reportes, fotos=None
    ):
        if not descripcion.strip():
            raise ValueError("La descripción del defecto es obligatoria.")

        reporte = ReporteDefecto(material, descripcion, fotos)
        reportes.append(reporte)
        return reporte
