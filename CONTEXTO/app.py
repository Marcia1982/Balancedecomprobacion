import os
import pandas as pd
from openai import OpenAI

def procesar_balance_y_generar_informe(ruta_excel):
    print("1. Leyendo el archivo de Excel...")
    # Omitimos las primeras 6 filas de encabezado institucional según tu formato
    df = pd.read_excel(ruta_excel, skiprows=6)
    
    # Limpiar espacios en los nombres de las columnas
    df.columns = df.columns.str.strip()
    
    # Filtrar filas vacías donde no haya código de cuenta
    df = df.dropna(subset=['Código'])
    
    # Extraer el primer dígito del código para clasificar contablemente
    df['Tipo_Cuenta'] = df['Código'].astype(str).str.slice(0, 1)
    
    # Asegurar que la columna 'Actual' sea numérica para sumar correctamente
    df['Actual'] = pd.to_numeric(df['Actual'], errors='coerce').fillna(0)
    
    # 2. Calcular los totales por categoría contable
    total_activos = df[df['Tipo_Cuenta'] == '1']['Actual'].sum()
    total_pasivos = df[df['Tipo_Cuenta'] == '2']['Actual'].sum()
    total_patrimonio = df[df['Tipo_Cuenta'] == '3']['Actual'].sum()
    total_ingresos = df[df['Tipo_Cuenta'] == '4']['Actual'].sum()
    total_gastos = df[df['Tipo_Cuenta'].isin(['5', '6'])]['Actual'].sum()
    
    # 3. Calcular las Razones Financieras Clave
    utilidad_neta = total_ingresos - total_gastos
    margen_neto = (utilidad_neta / total_ingresos) * 100 if total_ingresos != 0 else 0
    endeudamiento = (total_pasivos / total_activos) * 100 if total_activos != 0 else 0
    
    datos_financieros = {
        "Total_Activos": total_activos,
        "Total_Pasivos": total_pasivos,
        "Total_Patrimonio": total_patrimonio,
        "Ingresos_Totales": total_ingresos,
        "Gastos_Totales": total_gastos,
        "Utilidad_Neta": utilidad_neta,
        "Margen_Neto_Porcentaje": round(margen_neto, 2),
        "Endeudamiento_Porcentaje": round(endeudamiento, 2)
    }
    
    print("2. Razones financieras calculadas con éxito.")
    print(datos_financieros)
    
    print("3. Conectando con el Agente de IA para redactar el informe...")
    try:
        # Inicializar el cliente de la API (requiere tener tu variable de entorno configurada)
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        prompt = f"""
        Actúa como un director financiero (CFO) y analista contable experto. 
        Analiza los siguientes indicadores financieros calculados a partir del balance de comprobación de la empresa:

        - Total de Activos: ₡{datos_financieros['Total_Activos']:,.2f}
        - Total de Pasivos: ₡{datos_financieros['Total_Pasivos']:,.2f}
        - Total de Patrimonio: ₡{datos_financieros['Total_Patrimonio']:,.2f}
        - Ingresos Totales: ₡{datos_financieros['Ingresos_Totales']:,.2f}
        - Gastos Totales: ₡{datos_financieros['Gastos_Totales']:,.2f}
        - Utilidad Neta: ₡{datos_financieros['Utilidad_Neta']:,.2f}
        - Margen Neto: {datos_financieros['Margen_Neto_Porcentaje']}%
        - Nivel de Endeudamiento: {datos_financieros['Endeudamiento_Porcentaje']}%

        Por favor, genera un informe ejecutivo de salud financiera redactado en lenguaje claro, profesional y de fácil comprensión para la gerencia. El informe debe estructurarse obligatoriamente en:
        1. **Diagnóstico General:** ¿La empresa muestra estabilidad financiera?
        2. **Fortalezas:** Aspectos positivos destacados de los números.
        3. **Alertas y Recomendaciones:** Acciones contables o financieras sugeridas a corto plazo para mitigar riesgos.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente contable y financiero experto en análisis de empresas."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error al conectar con la API de IA: {str(e)}"

# --- BLOQUE DE EJECUCIÓN ---
if __name__ == "__main__":
    # Asegúrate de poner el nombre exacto de tu archivo Excel en la misma carpeta
    archivo_excel = "balance_comprobacion.xlsx"
    
    if os.path.exists(archivo_excel):
        informe_final = procesar_balance_y_generar_informe(archivo_excel)
        print("\n" + "="*50)
        print("INFORME FINANCIERO GENERADO POR EL AGENTE:")
        print("="*50)
        print(informe_final)
    else:
        print(f"No se encontró el archivo '{archivo_excel}'. Guárdalo en la misma carpeta del script.")