"""Pruebas de autenticación (login) del Validador Financiero AI.

Valida:
1. Entrar con credenciales correctas → redirige a /
2. Entrar con clave equivocada → muestra error, no dice cuál falló
3. Abrir pantalla principal sin haber entrado → redirige a /login
4. Salir y volver a intentar entrar → después de /salir, / redirige a /login
"""

import pytest


def test_login_exitoso_redirige_a_principal(client):
    """Credenciales correctas: debe iniciar sesión y redirigir a la pantalla principal."""
    resp = client.post("/login", data={"usuario": "admin", "clave": "Cambiar2026"}, follow_redirects=False)
    assert resp.status_code == 302
    assert resp.location == "/"


def test_login_clave_equivocada_muestra_error(client):
    """Clave incorrecta: debe mostrar error genérico sin revelar cuál falló."""
    resp = client.post("/login", data={"usuario": "admin", "clave": "clave_incorrecta"}, follow_redirects=True)
    html = resp.data.decode("utf-8")
    assert resp.status_code == 200
    assert "Usuario o contraseña incorrectos" in html
    # No debe revelar cuál de los dos falló por separado
    assert "usuario incorrecto" not in html.lower()
    assert "contraseña incorrecta" not in html.lower()


def test_pantalla_principal_sin_login_redirige(client):
    """Sin sesión: acceder a / debe redirigir a /login."""
    resp = client.get("/", follow_redirects=False)
    assert resp.status_code == 302
    assert "/login" in resp.location


def test_salir_y_volver_a_intentar_entrar(client):
    """Después de cerrar sesión, acceder a / debe redirigir a /login."""
    # Primero iniciamos sesión
    client.post("/login", data={"usuario": "admin", "clave": "Cambiar2026"})
    # Cerramos sesión
    resp = client.get("/salir", follow_redirects=False)
    assert resp.status_code == 302
    assert "/login" in resp.location
    # Ahora acceder a / debe redirigir a /login
    resp = client.get("/", follow_redirects=False)
    assert resp.status_code == 302
    assert "/login" in resp.location
