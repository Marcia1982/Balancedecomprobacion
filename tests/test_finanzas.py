"""Pruebas contra las cifras de control del archivo de prueba balance_comprobacion.xlsx.

Las cifras esperadas se calculan a partir de los datos del archivo de prueba:
- Activo (clase 1): EFECTIVOS 200.000 + BANCOS 150.000 = 350.000
- Pasivo (clase 2): PROVEEDORES 180.000 + PRESTAMOS BANCARIOS 130.000 = 310.000
- Patrimonio (clase 3): CAPITAL SOCIAL 500.000 = 500.000
- Ingresos (clase 4): VENTAS 1.000.000 = 1.000.000
- Gastos (clase 5/6): GASTOS ADMINISTRATIVOS -300.000 + GASTOS FINANCIEROS -50.000 = -350.000
- Utilidad Neta: 1.000.000 - (-350.000) = 1.350.000
- Margen Neto: 1.350.000 / 1.000.000 * 100 = 135.00%
- Endeudamiento: 310.000 / 350.000 * 100 = 88.57%
"""

import pytest


def test_total_activos(datos_balance):
    """Total de Activos debe ser 350.000,00."""
    datos, _, _ = datos_balance
    assert datos.Total_Activos == 350000.00


def test_total_pasivos(datos_balance):
    """Total de Pasivos debe ser 310.000,00."""
    datos, _, _ = datos_balance
    assert datos.Total_Pasivos == 310000.00


def test_total_patrimonio(datos_balance):
    """Total de Patrimonio debe ser 500.000,00."""
    datos, _, _ = datos_balance
    assert datos.Total_Patrimonio == 500000.00


def test_ingresos_totales(datos_balance):
    """Ingresos Totales debe ser 1.000.000,00."""
    datos, _, _ = datos_balance
    assert datos.Ingresos_Totales == 1000000.00


def test_gastos_totales(datos_balance):
    """Gastos Totales debe ser -350.000,00."""
    datos, _, _ = datos_balance
    assert datos.Gastos_Totales == -350000.00


def test_utilidad_neta(datos_balance):
    """Utilidad Neta debe ser 1.350.000,00."""
    datos, _, _ = datos_balance
    assert datos.Utilidad_Neta == 1350000.00


def test_margen_neto(datos_balance):
    """Margen Neto debe ser 135,00%."""
    datos, _, _ = datos_balance
    assert datos.Margen_Neto_Porcentaje == 135.00


def test_endeudamiento(datos_balance):
    """Endeudamiento debe ser 88,57%."""
    datos, _, _ = datos_balance
    assert datos.Endeudamiento_Porcentaje == 88.57


def test_filas_procesadas(datos_balance):
    """Debe procesar exactamente 8 filas con código válido."""
    _, filas, _ = datos_balance
    assert filas == 8


def test_no_excepciones_tipo(datos_balance):
    """Los cálculos no deben lanzar excepciones de tipo de datos."""
    datos, _, _ = datos_balance
    assert isinstance(datos.Total_Activos, float)
    assert isinstance(datos.Total_Pasivos, float)
    assert isinstance(datos.Total_Patrimonio, float)
    assert isinstance(datos.Ingresos_Totales, float)
    assert isinstance(datos.Gastos_Totales, float)
    assert isinstance(datos.Utilidad_Neta, float)
    assert isinstance(datos.Margen_Neto_Porcentaje, float)
    assert isinstance(datos.Endeudamiento_Porcentaje, float)
