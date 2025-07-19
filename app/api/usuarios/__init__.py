from flask import Blueprint
usuario_bp = Blueprint ("usuarios",__name__)
from . import routes