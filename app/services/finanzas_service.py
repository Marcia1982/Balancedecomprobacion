"""Servicio de finanzas: aplica las reglas de negocio R1-R5 sobre el Excel."""

import os
import pandas as pd

from app.models.balance import DatosFinancieros


def leer_y_procesar_balance(ruta_archivo: str):
    """
    Lee el Balance de Comprobación y aplica las reglas de negocio R1-R5.

    Retorna (DatosFinancieros, numero_de_filas_procesadas).
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

    # R3: extraer el primer dígito de Código para clasificar la cuenta contable
    df["Tipo_Cuenta"] = df["Código"].astype(str).str.slice(0, 1)

    # R4: columnas de saldos a numérico; vacíos o nulos = 0
    df["Actual"] = pd.to_numeric(df["Actual"], errors="coerce").fillna(0)

    # Cálculos estrictos por código (sin IA)
    total_activos = df[df["Tipo_Cuenta"] == "1"]["Actual"].sum()
    total_pasivos = df[df["Tipo_Cuenta"] == "2"]["Actual"].sum()
    total_patrimonio = df[df["Tipo_Cuenta"] == "3"]["Actual"].sum()
    total_ingresos = df[df["Tipo_Cuenta"] == "4"]["Actual"].sum()
    total_gastos = df[df["Tipo_Cuenta"].isin(["5", "6"])]["Actual"].sum()

    utilidad_neta = total_ingresos - total_gastos
    margen_neto = (utilidad_neta / total_ingresos) * 100 if total_ingresos != 0 else 0
    endeudamiento = (total_pasivos / total_activos) * 100 if total_activos != 0 else 0

    datos = DatosFinancieros(
        Total_Activos=round(float(total_activos), 2),
        Total_Pasivos=round(float(total_pasivos), 2),
        Total_Patrimonio=round(float(total_patrimonio), 2),
        Ingresos_Totales=round(float(total_ingresos), 2),
        Gastos_Totales=round(float(total_gastos), 2),
        Utilidad_Neta=round(float(utilidad_neta), 2),
        Margen_Neto_Porcentaje=round(float(margen_neto), 2),
        Endeudamiento_Porcentaje=round(float(endeudamiento), 2),
    )

    # Preparar filas para detalle por registro (Código, Descripción, Actual)
    filas_detalle = df[["Código", "Descripción", "Actual"]].copy()
    filas_detalle["Descripción"] = filas_detalle["Descripción"].str.strip()
    filas_detalle = filas_detalle.to_dict("records")

    return datos, len(df), filas_detalle
