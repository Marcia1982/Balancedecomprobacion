# Planteamiento del Proyecto (extraído del DOCX)

DOCUMENTO DE CONTEXTO · ValidadorFinancieroAI
1. Qué es esta app Aplicación web orientada a gerentes y contadores para automatizar la lectura de un Balance de Comprobación en Excel, calcular razones financieras exactas por código y generar un informe ejecutivo de salud financiera mediante un agente de IA.
2. El proceso hoy Actualmente, el contador extrae el Balance de Comprobación de un sistema contable en Excel, revisa manualmente las cuentas de mayor y calcula de forma analítica los ratios (margen neto, endeudamiento, liquidez). Este proceso toma entre 1 y 2 horas por periodo y requiere redactar manualmente el diagnóstico gerencial, lo que puede generar errores de transcripción o fatiga analítica.
3. Datos de entrada
Archivo o dato: Balance de Comprobación (formato Excel .xlsx). 
image_f5baad.png
De dónde sale: Exportación directa del sistema contable de la empresa. 
image_f5baad.png
Campos/Columnas clave: Código (para identificar cuentas por dígitos), Descripción y Actual (saldo actual de la cuenta). 
image_f5baad.png
4. Reglas de negocio para el código
R1: El sistema debe omitir las primeras 6 filas de encabezado institucional del archivo Excel. 
image_f5baad.png
R2: Se deben filtrar y descartar las filas que no tengan un código de cuenta válido. 
image_f5baad.png
R3: El código debe extraer el primer dígito de la columna Código para clasificar las cuentas contables (1: Activo, 2: Pasivo, 3: Patrimonio, 4: Ingresos, 5/6: Gastos). 
image_f5baad.png
R4: Las columnas de saldos deben transformarse a formato numérico, reemplazando valores vacíos o nulos por cero para evitar errores de cálculo. 
image_f5baad.png
R5: El sistema calculará matemáticamente el Margen Neto () y el Nivel de Endeudamiento () mediante código estricto para evitar alucinaciones de la IA. 
image_f5baad.png
5. Lo que hace el agente de IA
Rol: Director Financiero (CFO) y analista contable experto.
Qué recibe: Un diccionario estructurado con los totales calculados por Python (Activos, Pasivos, Patrimonio, Ingresos, Gastos, Utilidad Neta, Margen Neto y Endeudamiento). 
image_f5baad.png
Contrato JSON de salida:
diagnostico_general (string): Evaluación de la estabilidad financiera.
fortalezas (string): Aspectos positivos destacados de los números.
alertas_recomendaciones (string): Acciones sugeridas a corto plazo para mitigar riesgos.
Regla estricta: El agente nunca inventa datos; si un indicador no está disponible, escribe "no indicado".
6. Qué produce la app Una interfaz web sencilla en español que muestra los resultados numéricos de las razones financieras y el informe ejecutivo redactado por el agente en tres secciones claras (Diagnóstico, Fortalezas, Recomendaciones).
7. Quién decide El contador o la gerencia de la empresa, quienes revisan el informe generado por la IA para la toma de decisiones estratégicas.
8. Datos de prueba que hay que generar Un archivo Excel ficticio llamado balance_comprobacion.xlsx que contenga cuentas con códigos de la 1 a la 6, descripciones estándar y montos numéricos en la columna de saldos Actual para validar las sumatorias y los porcentajes. 
image_f5baad.png+ 1
9. Cifras de control Con el archivo de prueba, los cálculos de Python deben arrojar exactamente las sumas por clase contable y los porcentajes de margen y endeudamiento sin arrojar excepciones de tipo de datos.
10. Casos límite
Archivo Excel vacío o con formato incorrecto: El sistema debe capturar el error y mostrar un mensaje claro en pantalla.
Cuentas sin saldo numérico o celdas con texto en la columna Actual: El código debe tratarlas como cero automáticamente. 
image_f5baad.png
11. Reglas del sistema Python con Flask y patrón MVC gestionado con uv; la llave del agente en .env y nunca en el código; iniciar_app.bat para encender la app; pantallas sencillas en español; prohibido inventar reglas o campos que no estén en este documento.
12. Supuestos por confirmar Se asume que la estructura de columnas del Balance de Comprobación mantiene siempre las columnas Código, Descripción y Actual en las mismas posiciones relativas tras omitir el encabezado institucional. 
image_f5baad.png