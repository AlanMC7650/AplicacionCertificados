import psycopg2
from flask import current_app, g

def get_connection():
    if "db_c" not in g:
        # Importamos la app config para acceder a DATABASE_URL
        from .config import DevConfig  # O usa current_app.config si ya tenés app creada

        g.db_c = psycopg2.connect(DevConfig.SQLALCHEMY_DATABASE_URI)
    return g.db_c

def close_connection(e=None):
    db_c = g.pop("db_c", None)
    if db_c is not None:
        db_c.close()
