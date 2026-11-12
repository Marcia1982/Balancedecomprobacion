"""Regla R3: Extraer el primer dígito de Código para clasificar la cuenta contable."""

import pandas as pd


def aplicar_r3_clasificacion(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extrae el primer dígito de la columna Código para clasificar las cuentas:
    1: Activo, 2: Pasivo, 3: Patrimonio, 4: Ingresos, 5/6: Gastos.

    R3: El código debe extraer el primer dígito de la columna Código para
    clasificar las cuentas contables.
    """
    df = df.copy()
    df["Tipo_Cuenta"] = df["Código"].astype(str).str.slice(0, 1)
    return df
