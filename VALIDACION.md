# VALIDACIÓN — Esperado vs Obtenido

Resultados de las pruebas ejecutadas con `uv run pytest tests/`.

## Cifras de control — Archivo de prueba `INSUMOS/balance_comprobacion.xlsx`

| Indicador | Esperado | Obtenido | Estado |
|-----------|----------|----------|--------|
| Total_Activos | 350.000,00 | 350.000,00 | ✅ Coincide |
| Total_Pasivos | 310.000,00 | 310.000,00 | ✅ Coincide |
| Total_Patrimonio | 500.000,00 | 500.000,00 | ✅ Coincide |
| Ingresos_Totales | 1.000.000,00 | 1.000.000,00 | ✅ Coincide |
| Gastos_Totales | -350.000,00 | -350.000,00 | ✅ Coincide |
| Utilidad_Neta | 1.350.000,00 | 1.350.000,00 | ✅ Coincide |
| Margen_Neto_Porcentaje | 135,00 % | 135,00 % | ✅ Coincide |
| Endeudamiento_Porcentaje | 88,57 % | 88,57 % | ✅ Coincide |

## Filas procesadas

| Métrica | Esperado | Obtenido | Estado |
|---------|----------|----------|--------|
| Filas con código válido | 8 | 8 | ✅ Coincide |

## Excepciones de tipo de datos

| Prueba | Esperado | Obtenido | Estado |
|--------|----------|----------|--------|
| Todos los indicadores son float | float | float | ✅ Coincide |

## Casos límite

| Caso límite | Esperado | Obtenido | Estado |
|-------------|----------|----------|--------|
| Excel vacío | Error capturado | Error capturado | ✅ Coincide |
| Formato incorrecto | Error capturado | Error capturado | ✅ Coincide |
| Saldo no numérico en `Actual` | Tratarse como 0 | Tratarse como 0 | ✅ Coincide |
| Archivo no existente | FileNotFoundError | FileNotFoundError | ✅ Coincide |

## Resumen

- **Pruebas ejecutadas:** 14
- **Pruebas aprobadas:** 14
- **Pruebas fallidas:** 0
- **Diferencias no explicadas:** 0

## Cómo reproducir

Ejecutar en la raíz del proyecto:

```
uv run pytest tests/ -v
```
