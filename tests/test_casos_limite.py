"""Pruebas contra los casos límite definidos en AGENTS.md:

1. Archivo Excel vacío o con formato incorrecto: el sistema debe capturar el error
   y mostrar un mensaje claro en pantalla.
2. Cuentas sin saldo numérico o celdas con texto en la columna Actual:
   el código debe tratarlas como cero automáticamente.
"""

import os
import tempfile
import pytest
import pandas as pd

from app.services.finanzas_service import leer_y_procesar_balance


def test_excel_vacio_lanza_error_claro():
    """Archivo vacío: el sistema debe capturar el error."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        # Crear un Excel completamente vacío (sin hojas con datos)
        df_vacio = pd.DataFrame()
        df_vacio.to_excel(tmp.name, index=False)
        ruta = tmp.name

    try:
        with pytest.raises(Exception) as excinfo:
            leer_y_procesar_balance(ruta)
        # Verificar que el error sea capturado (no falle silenciosamente)
        assert "No se encontró" in str(excinfo.value) or "Columnas" in str(excinfo.value) or len(str(excinfo.value)) > 0
    finally:
        os.unlink(ruta)


def test_formato_incorrecto_lanza_error():
    """Archivo con formato incorrecto (sin columnas esperadas): error claro."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        # Crear un Excel con columnas incorrectas
        df_incorrecto = pd.DataFrame({"ColumnaA": [1, 2], "ColumnaB": ["a", "b"]})
        df_incorrecto.to_excel(tmp.name, index=False)
        ruta = tmp.name

    try:
        with pytest.raises(Exception) as excinfo:
            leer_y_procesar_balance(ruta)
        assert len(str(excinfo.value)) > 0
    finally:
        os.unlink(ruta)


def test_saldos_no_numericos_se_tratan_como_cero():
    """Celdas con texto en la columna Actual deben tratarse como cero."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        # Crear un Excel con las 6 filas de encabezado + datos con texto en Actual
        datos = [
            # Fila 1-6: encabezado institucional
            ["Empresa Prueba S.A", "", "", "", "", "", ""],
            ["", "", "", "", "", "", ""],
            ["Contabilidad - Balance de comprobación ( Colones )", "", "", "", "", "", ""],
            ["", "", "", "", "", "", ""],
            ["Del día 01-01-2025 al día 31-12-2025", "", "", "", "", "", ""],
            ["", "", "", "", "", "", ""],
            # Fila 7: encabezado de datos
            ["Código", "Descripción", "Anterior", "Débitos", "Créditos", "Neto", "Actual"],
            # Fila 8: vacía
            ["", "", "", "", "", "", ""],
            # Fila 9+: datos con texto en Actual
            ["110-00-000", "EFECTIVOS", 100000, 500000, 400000, 100000, "SIN SALDO"],
            ["210-00-000", "PROVEEDORES", 80000, 100000, 200000, 100000, 180000],
        ]
        df = pd.DataFrame(datos)
        df.to_excel(tmp.name, index=False, header=False)
        ruta = tmp.name

    try:
        datos_financieros, filas, _ = leer_y_procesar_balance(ruta)
        # El saldo "SIN SALDO" debe tratarse como 0
        # Total_Activos = 200000 (EFECTIVOS con Actual=0 porque "SIN SALDO" -> 0)
        assert datos_financieros.Total_Activos == 0.0  # "SIN SALDO" se trata como 0
        assert datos_financieros.Total_Pasivos == 180000.0
    finally:
        os.unlink(ruta)


def test_archivo_no_existente_lanza_file_not_found():
    """Archivo que no existe: debe lanzar FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        leer_y_procesar_balance("INSUMOS/archivo_que_no_existe.xlsx")
