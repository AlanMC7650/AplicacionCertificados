# Importamos la librería blueprint para el programa
from flask import Blueprint

# Creamos una instancia de la clas Blueprint
auth_bp = Blueprint("auth", __name__, template_folder="templates")

# De este mismo directorio importamos las rutas
from . import routes
