"""Controlador Flask: rutas de la aplicación."""

import os
import tempfile
from flask import Blueprint, render_template, request, current_app

from app.services.finanzas_service import leer_y_procesar_balance
from app.services.ia_service import generar_informe_ia

balance_bp = Blueprint("balance", __name__)

# Nombre del archivo en INSUMOS/ (según confirmación del usuario)
ARCHIVO_POR_DEFECTO = os.path.join("INSUMOS", "balance_comprobacion.xlsx")


@balance_bp.route("/", methods=["GET"])
def index():
    """Pantalla principal: formulario para subir el Balance de Comprobación."""
    return render_template("index.html")


@balance_bp.route("/procesar", methods=["POST"])
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
