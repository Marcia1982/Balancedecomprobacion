"""Punto de entrada WSGI para despliegue."""

import os
import sys

# Cargar las variables del archivo .env automáticamente
from dotenv import load_dotenv
load_dotenv()

# Asegurar que el directorio raíz esté en el path para importar el paquete app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import crear_app

application = crear_app()

if __name__ == "__main__":
    application.run()
