"""Punto de entrada de la aplicación Flask."""

import os
import sys
from datetime import timedelta

# Asegurar que el directorio raíz esté en el path para importar el paquete app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from flask import Flask

# Cargar variables de entorno desde .env
load_dotenv()

from app.controllers.balance_controller import balance_bp
from app.auth import verificar_variables_entorno


def crear_app() -> Flask:
    app = Flask(__name__)

    # Verificar que existan las variables de entorno requeridas
    faltantes = verificar_variables_entorno()
    if faltantes:
        nombres = ", ".join(faltantes)
        print(f"Faltan variables de entorno: {nombres}")
        # La app sigue arrancando pero las rutas protegidas no dejarán entrar

    app.secret_key = os.environ.get("SECRET_KEY")

    # Sesión expira a las 8 horas
    app.permanent_session_lifetime = timedelta(hours=8)

    app.register_blueprint(balance_bp)
    return app


def main():
    app = crear_app()
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)


if __name__ == "__main__":
    main()
