"""Regla R5: Calcular totales por clase contable y razones financieras."""

import pandas as pd


def aplicar_r5_calculos(df: pd.DataFrame) -> dict:
    """
    Calcula los totales por clase contable y las razones financieras clave.

    R5: El sistema calculará matemáticamente el Margen Neto y el Nivel de
    Endeudamiento mediante código estricto para evitar alucinaciones de la IA.

    Retorna un diccionario con los 8 indicadores financieros.
    """
    total_activos = df[df["Tipo_Cuenta"] == "1"]["Actual"].sum()
    total_pasivos = df[df["Tipo_Cuenta"] == "2"]["Actual"].sum()
    total_patrimonio = df[df["Tipo_Cuenta"] == "3"]["Actual"].sum()
    total_ingresos = df[df["Tipo_Cuenta"] == "4"]["Actual"].sum()
    total_gastos = df[df["Tipo_Cuenta"].isin(["5", "6"])]["Actual"].sum()

    utilidad_neta = total_ingresos - total_gastos
    margen_neto = (utilidad_neta / total_ingresos) * 100 if total_ingresos != 0 else 0
    endeudamiento = (total_pasivos / total_activos) * 100 if total_activos != 0 else 0

    return {
        "Total_Activos": round(float(total_activos), 2),
        "Total_Pasivos": round(float(total_pasivos), 2),
        "Total_Patrimonio": round(float(total_patrimonio), 2),
        "Ingresos_Totales": round(float(total_ingresos), 2),
        "Gastos_Totales": round(float(total_gastos), 2),
        "Utilidad_Neta": round(float(utilidad_neta), 2),
        "Margen_Neto_Porcentaje": round(float(margen_neto), 2),
        "Endeudamiento_Porcentaje": round(float(endeudamiento), 2),
    }
