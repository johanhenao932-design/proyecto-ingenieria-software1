# Pruebas básicas del sistema de inventarios.
# Cada prueba es una función que empieza por "test_" y usa "assert"
# para comprobar que el resultado es el esperado.

import pytest
from modelo.modelo import Administrador, Tecnico, Material


def crear_datos():
    """Crea un administrador, un técnico y un material de ejemplo."""
    admin = Administrador(1, "admin", "admin123")
    tecnico = Tecnico(2, "tecnico1", "tec123")
    material = Material("M001", "Taladro", 10, 2)
    material.actualizarEstado()
    return admin, tecnico, material


# ---------- Inicio de sesión ----------

def test_login_correcto():
    admin, _, _ = crear_datos()
    assert admin.iniciarSesion("admin123") is True


def test_login_con_contrasena_incorrecta():
    admin, _, _ = crear_datos()
    assert admin.iniciarSesion("mala") is False


# ---------- Inventario ----------

def test_ingresar_material_nuevo():
    admin, _, _ = crear_datos()
    materiales = []
    admin.ingresarMaterial(Material("M002", "Casco", 20, 5), materiales)
    assert len(materiales) == 1


def test_ingresar_material_existente_suma_stock():
    admin, _, material = crear_datos()
    materiales = [material]
    admin.ingresarMaterial(Material("M001", "Taladro", 5, 2), materiales)
    assert material.stock == 15


def test_estado_del_material():
    agotado = Material("A", "Cable", 0, 2)
    agotado.actualizarEstado()
    bajo = Material("B", "Cable", 2, 2)
    bajo.actualizarEstado()
    normal = Material("C", "Cable", 10, 2)
    normal.actualizarEstado()
    assert agotado.estado == "Agotado"
    assert bajo.estado == "Stock bajo"
    assert normal.estado == "Disponible"


# ---------- Asignación al técnico ----------

def test_asignar_material_descuenta_stock():
    admin, tecnico, material = crear_datos()
    admin.asignarMaterial(tecnico, material, 4, [])
    assert material.stock == 6


def test_no_se_puede_asignar_mas_del_stock():
    admin, tecnico, material = crear_datos()
    with pytest.raises(ValueError):
        admin.asignarMaterial(tecnico, material, 999, [])


# ---------- Devoluciones ----------

def test_devolver_material_en_buen_estado_vuelve_al_stock():
    admin, tecnico, material = crear_datos()
    asignacion = admin.asignarMaterial(tecnico, material, 4, [])
    tecnico.devolverMaterial(asignacion, 4, [])
    assert material.stock == 10


def test_devolver_material_defectuoso_no_vuelve_al_stock():
    admin, tecnico, material = crear_datos()
    asignacion = admin.asignarMaterial(tecnico, material, 4, [])
    tecnico.devolverMaterial(asignacion, 4, [], defectuoso=True)
    assert material.stock == 6


# ---------- Reporte de defectos ----------

def test_reporte_de_defecto_sin_descripcion_da_error():
    _, tecnico, material = crear_datos()
    with pytest.raises(ValueError):
        tecnico.devolverMaterialDefectuoso(material, "", [])
