"""Servicio de lectura del Balance de Comprobación (Reglas R1 y R2).

Lee el archivo de Excel desde INSUMOS/, omite las primeras 6 filas de
encabezado institucional (R1) y descarta las filas sin código de cuenta
válido (R2).
"""

import os
import pandas as pd


def leer_balance(ruta_archivo: str):
    """
    Lee el Balance de Comprobación aplicando R1 y R2.

    R1: Omitir las primeras 6 filas de encabezado institucional.
    R2: Filtrar y descartar filas que no tengan un código de cuenta válido.

    Retorna (DataFrame, numero_de_filas_procesadas, numero_de_columnas).
    Lanza FileNotFoundError si el archivo no existe.
    """
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_archivo}")

    # R1: omitir las primeras 6 filas de encabezado institucional
    df = pd.read_excel(ruta_archivo, skiprows=6)

    # Limpiar espacios en nombres de columnas
    df.columns = df.columns.str.strip()

    # R2: filtrar y descartar filas que no tengan código de cuenta válido
    df = df.dropna(subset=["Código"])

    return df, len(df), len(df.columns)


def leer_balance_por_defecto():
    """
    Lee el archivo de Balance de Comprobación por defecto desde INSUMOS/.

    Usa el nombre de archivo balance_comprobacion.xlsx según la
    especificación en AGENTS.md.
    """
    ruta = os.path.join("INSUMOS", "balance_comprobacion.xlsx")
    return leer_balance(ruta)
