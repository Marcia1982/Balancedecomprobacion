# AGENTS.md

## Qué es esta app

Aplicación web orientada a gerentes y contadores para automatizar la lectura de un Balance de Comprobación en Excel, calcular razones financieras exactas por código de cuenta y generar un informe ejecutivo de salud financiera mediante un agente de IA (rol: Director Financiero / CFO).

## Datos de entrada

Archivo de insumos (sin modificar nada dentro de la carpeta `INSUMOS`):

- **Nombre real del archivo en `INSUMOS/`:** `balance_comprobacion.xlsx.xlsx`
- **Nombre que espera la app / referencia en código:** `balance_comprobacion_xlsx`
- **Hoja:** `BC` (una sola hoja)
- **Dimensiones:** 545 filas × 7 columnas (rango A1:G545)

Encabezado institucional (filas 1–6, se omiten):
1. `Marcia S.A`
2. (vacío)
3. `Contabilidad - Balance de comprobación ( Colones )`
4. (vacío)
5. `Del día 01-01-2025 al día 31-12-2025`
6. (vacío)

Fila 7 (encabezado de datos): `Código`, `Descripción`, `Anterior`, `Débitos`, `Créditos`, `Neto`, `Actual`

Fila 8: (vacía)

Desde la fila 9: datos de cuentas (ej. `110-00-000-0000 | EFECTIVOS & EQUIVALENTES | ...`).

Columnas/ campos:
| Campo | Descripción |
|---|---|
| `Código` | Código de cuenta (para identificar cuentas por dígitos). Clasifica por el primer dígito. |
| `Descripción` | Nombre de la cuenta contable. |
| `Anterior` | Saldo anterior. |
| `Débitos` | Movimientos a débito. |
| `Créditos` | Movimientos a crédito. |
| `Neto` | Débito menos crédito del período. |
| `Actual` | Saldo actual de la cuenta (columna numérica clave para los cálculos). |

Después de omitir las 6 filas de encabezado y descartar filas sin `Código` válido: **509 filas con código válido** y 7 columnas.

## Reglas de negocio (código, sin IA)

R1: El sistema debe omitir las primeras 6 filas de encabezado institucional del archivo Excel.

R2: Se deben filtrar y descartar las filas que no tengan un código de cuenta válido.

R3: El código debe extraer el primer dígito de la columna `Código` para clasificar las cuentas contables:
- `1`: Activo
- `2`: Pasivo
- `3`: Patrimonio
- `4`: Ingresos
- `5` / `6`: Gastos

R4: Las columnas de saldos deben transformarse a formato numérico, reemplazando valores vacíos o nulos por cero para evitar errores de cálculo.

R5: El sistema calculará matemáticamente el Margen Neto y el Nivel de Endeudamiento mediante código estricto para evitar alucinaciones de la IA.

Cálculos realizados por código (Python/pandas):
- `Total_Activos` = suma de `Actual` donde primer dígito de `Código` == `1`
- `Total_Pasivos` = suma de `Actual` donde primer dígito de `Código` == `2`
- `Total_Patrimonio` = suma de `Actual` donde primer dígito de `Código` == `3`
- `Ingresos_Totales` = suma de `Actual` donde primer dígito de `Código` == `4`
- `Gastos_Totales` = suma de `Actual` donde primer dígito de `Código` ∈ [`5`, `6`]
- `Utilidad_Neta` = `Ingresos_Totales` − `Gastos_Totales`
- `Margen_Neto_Porcentaje` = (`Utilidad_Neta` / `Ingresos_Totales`) × 100 (si `Ingresos_Totales` ≠ 0, else 0)
- `Endeudamiento_Porcentaje` = (`Total_Pasivos` / `Total_Activos`) × 100 (si `Total_Activos` ≠ 0, else 0)

## Lo que hace el agente de IA (con el contrato JSON)

Rol: Director Financiero (CFO) y analista contable experto.

Qué recibe: un diccionario estructurado con los totales calculados por Python (`Total_Activos`, `Total_Pasivos`, `Total_Patrimonio`, `Ingresos_Totales`, `Gastos_Totales`, `Utilidad_Neta`, `Margen_Neto_Porcentaje`, `Endeudamiento_Porcentaje`).

Contrato JSON de salida:

```json
{
  "diagnostico_general": "string",
  "fortalezas": "string",
  "alertas_recomendaciones": "string"
}
```

- `diagnostico_general` (string): Evaluación de la estabilidad financiera.
- `fortalezas` (string): Aspectos positivos destacados de los números.
- `alertas_recomendaciones` (string): Acciones sugeridas a corto plazo para mitigar riesgos.

Regla estricta: el agente nunca inventa datos; si un indicador no está disponible, escribe "no indicado".

## Qué produce la app

Una interfaz web sencilla en español que muestra los resultados numéricos de las razones financieras y el informe ejecutivo redactado por el agente en tres secciones claras: Diagnóstico, Fortalezas y Recomendaciones.

## Quién decide

El contador o la gerencia de la empresa, quienes revisan el informe generado por la IA para la toma de decisiones estratégicas.

## Cifras de control

Con el archivo de prueba, los cálculos de Python deben arrojar exactamente las sumas por clase contable y los porcentajes de margen y endeudamiento sin arrojar excepciones de tipo de datos.

## Casos límite

- Archivo Excel vacío o con formato incorrecto: el sistema debe capturar el error y mostrar un mensaje claro en pantalla.
- Cuentas sin saldo numérico o celdas con texto en la columna `Actual`: el código debe tratarlas como cero automáticamente.

## Reglas del sistema

- Python con Flask y patrón MVC gestionado con `uv`.
- La llave del agente en `.env` y nunca en el código.
- `iniciar_app.bat` para encender la app.
- Pantallas sencillas en español.
- Prohibido inventar reglas o campos que no estén en este documento.

## Supuesto confirmado

Las columnas `Código`, `Descripción` y `Actual` mantienen siempre las mismas posiciones relativas tras omitir el encabezado institucional.
