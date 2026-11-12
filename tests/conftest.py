"""Configuración de pytest y fixtures para el proyecto Validador Financiero AI."""

import sys
import os

# Configurar pythonpath para que pytest pueda importar los módulos de la app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app.services.finanzas_service import leer_y_procesar_balance

RUTA_PRUEBA = os.path.join("INSUMOS", "balance_comprobacion.xlsx")


@pytest.fixture
def datos_balance():
    """Fixture que lee y procesa el archivo de prueba."""
    datos, filas, filas_detalle = leer_y_procesar_balance(RUTA_PRUEBA)
    return datos, filas, filas_detalle
