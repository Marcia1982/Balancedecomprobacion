"""Punto de entrada de la aplicación Flask."""

import os
import sys

# Asegurar que el directorio raíz esté en el path para importar el paquete app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask

from app.controllers.balance_controller import balance_bp


def crear_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-cambiar-en-produccion")
    app.register_blueprint(balance_bp)
    return app


def main():
    app = crear_app()
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "1") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)


if __name__ == "__main__":
    main()
