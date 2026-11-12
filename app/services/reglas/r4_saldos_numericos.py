"""Regla R4: Transformar saldos a formato numérico (vacíos/nulos = 0)."""

import pandas as pd


def aplicar_r4_saldos_numericos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforma la columna Actual a formato numérico, reemplazando valores
    vacíos o nulos por cero.

    R4: Las columnas de saldos deben transformarse a formato numérico,
    reemplazando valores vacíos o nulos por cero para evitar errores de cálculo.
    """
    df = df.copy()
    df["Actual"] = pd.to_numeric(df["Actual"], errors="coerce").fillna(0)
    return df
