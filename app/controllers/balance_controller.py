"""Controlador Flask: rutas de la aplicación."""

import os
import tempfile
import hmac
from flask import Blueprint, render_template, request, session, redirect, url_for, flash

from app.services.finanzas_service import leer_y_procesar_balance
from app.services.ia_service import generar_informe_ia
from app.auth import login_requerido, verificar_credenciales

balance_bp = Blueprint("balance", __name__)

# Nombre del archivo en INSUMOS/ (según confirmación del usuario)
ARCHIVO_POR_DEFECTO = os.path.join("INSUMOS", "balance_comprobacion.xlsx")


# --- Autenticación ---

@balance_bp.route("/login", methods=["GET"])
def login():
    """Pantalla de login: formulario con usuario y contraseña."""
    return render_template("login.html")


@balance_bp.route("/login", methods=["POST"])
def login_post():
    """Procesa el login: compara con APP_USUARIO y APP_CLAVE de forma segura."""
    usuario = request.form.get("usuario", "")
    clave = request.form.get("clave", "")

    if verificar_credenciales(usuario, clave):
        session["usuario_autenticado"] = True
        session.permanent = True  # expira según PERMANENT_SESSION_LIFETIME
        return redirect(url_for("balance.index"))

    flash("Usuario o contraseña incorrectos", "error")
    return render_template("login.html")


@balance_bp.route("/salir")
def salir():
    """Borra la sesión y redirige al login."""
    session.pop("usuario_autenticado", None)
    return redirect(url_for("balance.login"))


# --- Rutas protegidas ---

@balance_bp.route("/", methods=["GET"])
@login_requerido
def index():
    """Pantalla principal: formulario para subir el Balance de Comprobación."""
    return render_template("index.html")


@balance_bp.route("/procesar", methods=["POST"])
@login_requerido
def procesar():
    """Recibe el Excel, aplica reglas de negocio y genera el informe de IA."""
    archivo = request.files.get("archivo_excel")

    # Si no se subió archivo, intentar usar el por defecto en INSUMOS/
    if not archivo or archivo.filename == "":
        ruta = ARCHIVO_POR_DEFECTO
        nombre_archivo = os.path.basename(ruta)
        archivo_subido = False
    else:
        nombre_archivo = archivo.filename
        archivo_subido = True
        # Guardar el archivo subido en una ruta temporal para leerlo con pandas
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
        archivo.save(tmp.name)
        ruta = tmp.name

    try:
        datos, filas_procesadas, filas_detalle = leer_y_procesar_balance(ruta)
    except FileNotFoundError as e:
        return render_template(
            "index.html",
            error=str(e),
            nombre_archivo=nombre_archivo,
        )
    except Exception as e:
        return render_template(
            "index.html",
            error=f"Error al procesar el archivo: {str(e)}",
            nombre_archivo=nombre_archivo,
        )

    informe_ia = generar_informe_ia(datos.a_diccionario())

    return render_template(
        "resultado.html",
        nombre_archivo=nombre_archivo,
        filas_procesadas=filas_procesadas,
        datos=datos.a_diccionario(),
        informe=informe_ia,
        filas_detalle=filas_detalle,
        archivo_subido=archivo_subido,
    )
