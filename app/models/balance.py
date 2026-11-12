"""Modelo de datos del Balance de Comprobación."""

from dataclasses import dataclass


@dataclass
class DatosFinancieros:
    """Totales y razones financieras calculados por código (reglas R1-R5)."""

    Total_Activos: float
    Total_Pasivos: float
    Total_Patrimonio: float
    Ingresos_Totales: float
    Gastos_Totales: float
    Utilidad_Neta: float
    Margen_Neto_Porcentaje: float
    Endeudamiento_Porcentaje: float

    def a_diccionario(self) -> dict:
        return {
            "Total_Activos": self.Total_Activos,
            "Total_Pasivos": self.Total_Pasivos,
            "Total_Patrimonio": self.Total_Patrimonio,
            "Ingresos_Totales": self.Ingresos_Totales,
            "Gastos_Totales": self.Gastos_Totales,
            "Utilidad_Neta": self.Utilidad_Neta,
            "Margen_Neto_Porcentaje": self.Margen_Neto_Porcentaje,
            "Endeudamiento_Porcentaje": self.Endeudamiento_Porcentaje,
        }
