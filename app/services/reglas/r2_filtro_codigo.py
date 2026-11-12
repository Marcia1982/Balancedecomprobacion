"""Regla R2: Filtrar y descartar filas sin código de cuenta válido."""

import pandas as pd


def aplicar_r2_filtro_codigo(df: pd.DataFrame) -> pd.DataFrame:
    """
    Descarta las filas que no tengan un código de cuenta válido.

    R2: Se deben filtrar y descartar las filas que no tengan un código de
    cuenta válido.
    """
    return df.dropna(subset=["Código"])
