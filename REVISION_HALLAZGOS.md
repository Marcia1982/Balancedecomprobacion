# Informe de Hallazgos — Revisor

Revisión de código y plantillas del proyecto `balance_comprobacion`.
Generado por el subagente **@revisor** (sin modificar ningún archivo).

---

## Hallazgo 1 — Falta `.gitignore` (Prioridad: ALTA)

**Descripción:** No existe un archivo `.gitignore` en la raíz del proyecto. Esto podría permitir subir accidentalmente a GitHub archivos sensibles como `.env` (que contiene `OPENAI_API_KEY`) y el entorno virtual `.venv/`.

**Archivo afectado:** Raíz del proyecto (archivo ausente)

**Corrección propuesta:** Crear `.gitignore` con al menos:
```
.env
.venv/
__pycache__/
*.pyc
.env
.pytest_cache/
.DS_Store
```

---

## Hallazgo 2 — `secret_key` con valor por defecto escrito en el código (Prioridad: MEDIA)

**Descripción:** En `app/main.py` línea 11, la `secret_key` de Flask tiene un valor por defecto escrito directamente en el código: `"dev-secret-key-cambiar-en-produccion"`. Aunque se lee primero de `os.environ.get("FLASK_SECRET_KEY")`, el valor por defecto está expuesto en el código fuente.

**Archivo afectado:** `app/main.py`, línea 11

**Corrección propuesta:** Eliminar el valor por defecto o hacer que sea obligatorio configurar `FLASK_SECRET_KEY` en `.env`. Ejemplo:
```python
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
if not app.secret_key:
    raise ValueError("FLASK_SECRET_KEY debe estar configurada en .env")
```

---

## Hallazgo 3 — `OPENAI_API_KEY` leída correctamente de `.env` (Prioridad: BAJA — informativo)

**Descripción:** La clave de OpenAI se lee correctamente desde la variable de entorno `OPENAI_API_KEY` en `app/services/ia_service.py`. No está escrita directamente en el código. El archivo `.env` contiene un placeholder `"tu_clave_de_openai_aqui"` que debe ser reemplazado por el usuario.

**Archivo afectado:** `app/services/ia_service.py`, líneas 23-24; `.env`

**Estado:** Correcto, sin acción requerida hasta que el usuario configure su clave real.

---

## Hallazgo 4 — Conformidad con `AGENTS.md` (Prioridad: BAJA — informativo)

**Descripción:** Se revisó que todo lo construido esté documentado en `AGENTS.md`:
- ✅ Columnas utilizadas: `Código`, `Descripción`, `Anterior`, `Débitos`, `Créditos`, `Neto`, `Actual` (todas documentadas)
- ✅ Reglas de negocio R1-R5 implementadas según `AGENTS.md`
- ✅ Contrato JSON del agente IA con las 3 claves definidas
- ✅ Flask + patrón MVC + `uv`
- ✅ `iniciar_app.bat` para encender la app
- ✅ Pantallas en español
- ✅ Llave del agente en `.env` (no en el código)

**No se encontraron columnas, archivos o reglas inventadas que no estén en `AGENTS.md`.**

---

## Resumen

| Prioridad | Cantidad | Hallazgos |
|-----------|----------|-----------|
| ALTA | 1 | Falta `.gitignore` |
| MEDIA | 1 | `secret_key` con valor por defecto en código |
| BAJA | 2 | `OPENAI_API_KEY` correcta; conformidad con `AGENTS.md` |

**Acción requerida antes de subir a GitHub:** Crear `.gitignore` y revisar el `secret_key` en `app/main.py`.
