"""Servicio de IA: agente con rol CFO que devuelve el contrato JSON."""

import json
import os
import re

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def generar_informe_ia(datos_financieros: dict) -> dict:
    """
    Llama al agente de IA (Director Financiero / CFO) y devuelve el contrato JSON:
    {
        "diagnostico_general": "string",
        "fortalezas": "string",
        "alertas_recomendaciones": "string"
    }
    Regla estricta: nunca inventa datos; si un indicador no está disponible, escribe "no indicado".
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key or api_key == "tu_clave_de_openai_aqui":
        return {
            "diagnostico_general": "no indicado",
            "fortalezas": "no indicado",
            "alertas_recomendaciones": "no indicado: OPENAI_API_KEY no configurada en .env",
        }

    try:
        client = OpenAI(api_key=api_key)

        prompt = f"""Actúa como un director financiero (CFO) y analista contable experto.
Analiza los siguientes indicadores financieros calculados a partir del balance de comprobación de la empresa:

- Total de Activos: ₡{datos_financieros['Total_Activos']:,.2f}
- Total de Pasivos: ₡{datos_financieros['Total_Pasivos']:,.2f}
- Total de Patrimonio: ₡{datos_financieros['Total_Patrimonio']:,.2f}
- Ingresos Totales: ₡{datos_financieros['Ingresos_Totales']:,.2f}
- Gastos Totales: ₡{datos_financieros['Gastos_Totales']:,.2f}
- Utilidad Neta: ₡{datos_financieros['Utilidad_Neta']:,.2f}
- Margen Neto: {datos_financieros['Margen_Neto_Porcentaje']}%
- Nivel de Endeudamiento: {datos_financieros['Endeudamiento_Porcentaje']}%

Genera un informe ejecutivo de salud financiera en lenguaje claro, profesional y de fácil comprensión para la gerencia. El informe debe estructurarse obligatoriamente en:
1. Diagnóstico General: ¿La empresa muestra estabilidad financiera?
2. Fortalezas: Aspectos positivos destacados de los números.
3. Alertas y Recomendaciones: Acciones contables o financieras sugeridas a corto plazo para mitigar riesgos.

Responde exclusivamente con un objeto JSON válido con estas tres claves:
- diagnostico_general (string)
- fortalezas (string)
- alertas_recomendaciones (string)

Regla estricta: nunca inventes datos; si un indicador no está disponible, escribe "no indicado"."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Eres un asistente contable y financiero experto en análisis de empresas."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )

        contenido = response.choices[0].message.content or ""

        # Intentar parsear como JSON puro
        try:
            return json.loads(contenido)
        except json.JSONDecodeError:
            # Intentar extraer un bloque JSON embebido
            match = re.search(r"\{.*\}", contenido, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(0))
                except json.JSONDecodeError:
                    pass
            return {
                "diagnostico_general": contenido.strip() or "no indicado",
                "fortalezas": "no indicado",
                "alertas_recomendaciones": "no indicado",
            }

    except Exception as e:
        return {
            "diagnostico_general": "no indicado",
            "fortalezas": "no indicado",
            "alertas_recomendaciones": f"Error al conectar con la API de IA: {str(e)}",
        }
