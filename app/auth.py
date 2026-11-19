"""Autenticación de la aplicación Validador Financiero AI.

Lee las credenciales del administrador desde variables de entorno
(NUNCA escritas en el código). Proporciona un decorador para proteger rutas.
"""

import os
import hmac
from functools import wraps
from flask import session, redirect, url_for


def verificar_variables_entorno():
    """Verifica que existan las 3 variables de entorno requeridas.

    Retorna True si todas están presentes, False si falta alguna.
    """
    requeridas = ["APP_USUARIO", "APP_CLAVE", "SECRET_KEY"]
    faltantes = [v for v in requeridas if not os.environ.get(v)]
    return faltantes


def login_requerido(f):
    """Decorador que protege rutas exigiendo haber iniciado sesión.

    Si el usuario no ha iniciado sesión, redirige a /login.
    """

    @wraps(f)
    def decorada(*args, **kwargs):
        if not session.get("usuario_autenticado"):
            return redirect(url_for("balance.login"))
        return f(*args, **kwargs)

    return decorada


def verificar_credenciales(usuario: str, clave: str) -> bool:
    """Compara usuario y contraseña con las variables de entorno usando
    comparación segura (hmac.compare_digest) para evitar ataques de tiempo.

    Retorna True si coinciden ambas, False en caso contrario.
    """
    usuario_valido = os.environ.get("APP_USUARIO", "")
    clave_valida = os.environ.get("APP_CLAVE", "")

    if not usuario_valido or not clave_valida:
        return False

    usuario_ok = hmac.compare_digest(usuario, usuario_valido)
    clave_ok = hmac.compare_digest(clave, clave_valida)

    return usuario_ok and clave_ok
