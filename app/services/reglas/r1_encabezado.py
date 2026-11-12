"""Regla R1: Omitir las primeras 6 filas de encabezado institucional."""

import pandas as pd


def aplicar_r1_encabezado(ruta_archivo: str) -> pd.DataFrame:
    """
    Lee el Excel omitiendo las primeras 6 filas de encabezado institucional.

    R1: El sistema debe omitir las primeras 6 filas de encabezado institucional
    del archivo Excel.
    """
    df = pd.read_excel(ruta_archivo, skiprows=6)
    df.columns = df.columns.str.strip()
    return df
