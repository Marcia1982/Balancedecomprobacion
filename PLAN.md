# PLAN.md — Validador Financiero AI

Plan de entregas por subagente para el proyecto `balance_comprobacion`.
Generado por el subagente **@arquitecto** tras leer `AGENTS.md`, `CONTEXTO/` e `INSUMOS/`.

---

## 1. RESUMEN (5 líneas)

Vamos a construir una aplicación web en Flask (Python, patrón MVC, gestionado con `uv`) para gerentes y contadores. Entra un Balance de Comprobación en Excel desde `INSUMOS/` y la app calcula razones financieras exactas por código de cuenta. El agente de IA (rol CFO) recibe los totales calculados y devuelve un informe ejecutivo en JSON con diagnóstico, fortalezas y alertas/recomendaciones. Sale una interfaz en español con los números, el informe de la IA y mensajes de error para casos límite.

---

## 2. LO QUE ENCONTRÉ

### En CONTEXTO/
- `Planteamiento del Proyecto.docx` (documento de origen del proyecto, "ValidadorFinancieroAI")
- `Contexto_Mi_App.md` (texto extraído del DOCX: 44 párrafos, 0 tablas)
- `app.py` (script legacy simple que llama a OpenAI directamente, sin Flask MVC)

### En INSUMOS/
- Un solo archivo: `balance_comprobacion.xlsx.xlsx` (doble extensión `.xlsx.xlsx` en disco)
  - **Nota:** el usuario indica que el nombre esperado es `balance_comprobacion.xlsx` (sin doble extensión). Verificar antes de codificar.
- Hoja única `BC`, 545 filas × 7 columnas (rango A1:G545)
- Encabezado institucional en filas 1–6 (`Marcia S.A`, título, período `01-01-2025 al 31-12-2025`)
- Encabezado de datos en fila 7: `Código`, `Descripción`, `Anterior`, `Débitos`, `Créditos`, `Neto`, `Actual`
- Fila 8 vacía; datos desde fila 9
- 509 filas con código válido después de omitir encabezado y filtrar

### ¿Coincide con AGENTS.md?
- Sí en columnas clave (`Código`, `Descripción`, `Actual` están presentes)
- Sí en omitir 6 filas de encabezado (coincide con filas 1–6 del Excel real)
- Sí en clasificación por primer dígito (los códigos empiezan en `110…`, dígito 1 = Activo)
- **No cuadra el nombre del archivo:** `AGENTS.md` y `app.py` esperan `balance_comprobacion.xlsx`, pero el archivo real en disco es `balance_comprobacion.xlsx.xlsx`. El usuario confirma que el nombre esperado es `balance_comprobacion.xlsx`.

### Qué falta o no cuadra
- Falta `wsgi.py` para despliegue
- Falta carpeta `tests/` con pruebas pytest
- Falta `VALIDACION.md` (esperado vs obtenido)
- Falta `.gitignore` para evitar subir `.env` y `.venv/` a GitHub
- El `app.py` legacy no sigue el patrón MVC requerido por `AGENTS.md`
- Falta archivo de prueba ficticio `balance_comprobacion.xlsx` en `INSUMOS/` (solicitado por el usuario)

---

## 3. ENTREGAS POR SUBAGENTE (orden de ejecución)

### Fase 1 — @backend (estructura y datos)

| N° | Responsable | Qué debe entregar | Archivos que crea o modifica | Qué recibe de la entrega anterior | Cómo se verifica en pantalla |
|----|-------------|-------------------|------------------------------|-----------------------------------|------------------------------|
| 1 | @backend | Estructura base MVC con `uv`: `create_app()`, blueprint, `wsgi.py`, `iniciar_app.bat` que abre el navegador y enciende la app | `app/__init__.py`, `wsgi.py`, `iniciar_app.bat` (modifica), `pyproject.toml` (verifica) | `AGENTS.md` | Ejecutar `.\iniciar_app.bat`, abrir `http://localhost:5000`, ver la app en línea |
| 2 | @backend | Lectura de insumos: omitir 6 filas de encabezado, leer columnas (`Código`, `Descripción`, `Anterior`, `Débitos`, `Créditos`, `Neto`, `Actual`), contar filas con código válido. Usar nombre de archivo `balance_comprobacion.xlsx` (según confirmación del usuario) | `app/services/lectura_service.py` (nuevo) | `INSUMOS/balance_comprobacion.xlsx`, `AGENTS.md` | Ejecutar lectura, ver en consola: "509 filas con código válido, 7 columnas" |
| 3 | @backend | Regla R1: omitir las primeras 6 filas de encabezado institucional | `app/services/reglas/r1_encabezado.py` (nuevo) | Entrega 2 | Ejecutar R1 sobre el Excel, verificar que las filas 1–6 no aparezcan en los datos |
| 4 | @backend | Regla R2: filtrar y descartar filas sin `Código` válido | `app/services/reglas/r2_filtro_codigo.py` (nuevo) | Entrega 3 | Verificar que no queden filas sin `Código` |
| 5 | @backend | Regla R3: extraer primer dígito de `Código` y clasificar (1 Activo, 2 Pasivo, 3 Patrimonio, 4 Ingresos, 5/6 Gastos) | `app/services/reglas/r3_clasificacion.py` (nuevo) | Entrega 4 | Verificar columna `Tipo_Cuenta` con valores `1`–`6` |
| 6 | @backend | Regla R4: transformar saldos a numérico, vacíos/nulos = 0 | `app/services/reglas/r4_saldos_numericos.py` (nuevo) | Entrega 5 | Verificar que `Actual` sea numérico y no haya NaN |
| 7 | @backend | Regla R5: calcular totales por clase contable y razones (Margen Neto, Endeudamiento) | `app/services/reglas/r5_calculos.py` (nuevo) | Entrega 6 | Ver en consola los 8 indicadores calculados (Total_Activos, Total_Pasivos, etc.) |
| 8 | @backend | Integración agente de IA: leer `OPENAI_API_KEY` de `.env` (modo "no indicado" si no está configurada), enviar diccionario de totales, recibir contrato JSON (`diagnostico_general`, `fortalezas`, `alertas_recomendaciones`) | `app/services/ia_service.py` (modifica), `.env` (verifica placeholder) | Entrega 7 | Ver en consola el JSON con las 3 claves (o "no indicado" si no hay API key) |
| 9 | @backend | Controlador y rutas: `GET /` (inicio), `POST /procesar` (lee Excel, aplica reglas, llama a IA, renderiza resultados) | `app/controllers/balance_controller.py` (modifica), `app/main.py` (verifica) | Entrega 8 | Abrir `http://localhost:5000`, subir Excel, ver pantalla de resultados |
| 10 | @backend | Crear archivo de prueba ficticio `balance_comprobacion.xlsx` en `INSUMOS/` con cuentas de códigos 1-6, descripciones estándar y montos numéricos en `Actual` | `INSUMOS/balance_comprobacion.xlsx` (nuevo, dentro de INSUMOS/) | `AGENTS.md` (punto 8: datos de prueba) | Verificar que el archivo existe en `INSUMOS/` y que la app lo lee correctamente |

### Fase 2 — @frontend (pantallas)

| N° | Responsable | Qué debe entregar | Archivos que crea o modifica | Qué recibe de la entrega anterior | Cómo se verifica en pantalla |
|----|-------------|-------------------|------------------------------|-----------------------------------|------------------------------|
| 11 | @frontend | Pantalla de inicio: formulario para subir Excel, mensaje de bienvenida en español | `app/templates/index.html` (modifica) | Entrega 9 | Abrir `http://localhost:5000`, ver formulario con input de archivo y botón "Procesar" |
| 12 | @frontend | Pantalla de resultados: tablero con contadores grandes (8 indicadores) y tabla de razones financieras | `app/templates/resultado.html` (modifica) | Entrega 9 | Después de procesar, ver los 8 números en pantalla con formato moneda y porcentajes |
| 13 | @frontend | Detalle por registro: tabla con filas del balance (Código, Descripción, Actual) y filtro de búsqueda | `app/templates/resultado.html` (modifica) | Entrega 12 | En pantalla de resultados, ver tabla con registros y un campo de filtro que filtre al escribir |
| 14 | @frontend | Estilo de la app: fondo oscuro, pantallas profesionales en español, CSS embebido en `base.html`, sin librerías JS externas | `app/templates/base.html` (modifica), `app/static/` (CSS si aplica) | Entrega 13 | Ver la app completa con fondo oscuro, texto en español, sin librerías JS externas cargadas |

### Fase 3 — @tester (pruebas y validación)

| N° | Responsable | Qué debe entregar | Archivos que crea o modifica | Qué recibe de la entrega anterior | Cómo se verifica en pantalla |
|----|-------------|-------------------|------------------------------|-----------------------------------|------------------------------|
| 15 | @tester | Pruebas en `tests/` contra cifras de control: verificar que los 8 indicadores coincidan con el esperado y no lancen excepciones de tipo | `tests/test_finanzas.py` (nuevo), `tests/conftest.py` (nuevo) | Entrega 7 (cálculos de backend) | Ejecutar `uv run pytest tests/`, ver "X passed" sin fallos |
| 16 | @tester | Pruebas contra casos límite: Excel vacío, formato incorrecto, saldos no numéricos en `Actual` (tratar como cero) | `tests/test_casos_limite.py` (nuevo) | Entrega 15 | Ejecutar `uv run pytest tests/`, ver que los casos límite no rompen la app |
| 17 | @tester | `VALIDACION.md`: tabla con esperado vs obtenido para cada cifra de control y cada caso límite | `VALIDACION.md` (nuevo) | Entrega 16 | Abrir `VALIDACION.md`, ver filas con "esperado" y "obtenido" coincidiendo o diferencia explicada |

### Fase 4 — @revisor (revisión sin modificar)

| N° | Responsable | Qué debe entregar | Archivos que crea o modifica | Qué recibe de la entrega anterior | Cómo se verifica en pantalla |
|----|-------------|-------------------|------------------------------|-----------------------------------|------------------------------|
| 18 | @revisor | Revisión de seguridad: llaves expuestas, datos sensibles en código, `.gitignore` para `.env` y `.venv/` | Informe de hallazgos (nuevo, no modifica código) | Todas las entregas anteriores | Leer el informe de hallazgos, ver prioridad y corrección propuesta |
| 19 | @revisor | Revisión de conformidad: todo lo construido esté documentado en `AGENTS.md`, no haya columnas/inventos fuera de él | Informe de hallazgos (nuevo, no modifica código) | Todas las entregas anteriores | Leer el informe, verificar que no haya reglas o campos no documentados en `AGENTS.md` |

---

## 4. PUNTOS DE CONTROL

| Después de la entrega | Quién interviene | Qué debe ver el usuario en pantalla |
|-----------------------|------------------|-------------------------------------|
| 2 (lectura de insumos) | @tester | Consola muestra: "509 filas con código válido, 7 columnas" |
| 7 (cálculos R5) | @tester | Los 8 indicadores calculados sin excepciones de tipo (ej. Total_Activos: 3,044,685,365.71) |
| 8 (integración IA) | @tester | JSON con claves `diagnostico_general`, `fortalezas`, `alertas_recomendaciones` (o "no indicado" si no hay API key) |
| 11 (pantalla resultados) | @tester | Tablero con 8 contadores grandes y tabla de razones financieras en español |
| 17 (VALIDACION.md) | @revisor | `VALIDACION.md` muestra esperado vs obtenido, sin diferencias no explicadas |
| 18-19 (revisor) | @revisor | Informe de hallazgos con prioridad; si hay prioridad alta, corregir antes de considerar el proyecto listo |

---

## 5. RIESGOS

| Riesgo | Qué hará cada subagente si pasa |
|--------|---------------------------------|
| Datos incompletos (Excel vacío o sin filas con código) | @backend captura el error y muestra mensaje claro en pantalla (caso límite de AGENTS.md). @tester escribe prueba que verifique el mensaje. @revisor confirma que no haya fallo silencioso. |
| Archivo escaneado (PDF sin texto) | No aplica directamente (el insumo es Excel). Si en el futuro se recibe PDF escaneado, @arquitecto debe actualizar `AGENTS.md` antes de que @backend lo implemente; nunca inventar soporte no documentado. |
| Respuesta del agente de IA que no es JSON válido | @backend implementa fallback: intentar parsear JSON, si falla devolver `diagnostico_general: "no indicado"` y los demás campos con "no indicado" o el error. @tester prueba con respuesta malformada. |
| Límite de la llave gratis de OpenAI | @backend lee la llave de `.env` y, si no está configurada o retorna error, devuelve "no indicado" en los campos de IA sin romper la app. @revisor verifica que la llave no esté escrita en el código. |
| Nombre de archivo con doble extensión en disco | @backend usa el nombre `balance_comprobacion.xlsx` según confirmación del usuario. Si el archivo real en disco es `.xlsx.xlsx`, @arquitecto debe coordinar con el usuario antes de codificar. @revisor confirma que no se modificó nada en `INSUMOS/` excepto el archivo de prueba solicitado. |

---

## 6. PREGUNTAS PARA MÍ (respondidas)

1. **Nombre del archivo:** `balance_comprobacion.xlsx` (sin doble extensión), según confirmación del usuario.
2. **API key de OpenAI:** "no indicado" por ahora; el usuario configurará `.env` después.
3. **Archivo de prueba:** Sí, crear archivo ficticio `balance_comprobacion.xlsx` dentro de `INSUMOS/` con cuentas de códigos 1-6.
4. **Puerto:** 5000 por defecto.

---

**Siguiente paso:** Espero tu aprobación de esta tabla de entregas actualizada antes de que cualquier subagente comience a construir. No he modificado ningún archivo distinto de este `PLAN.md`.
