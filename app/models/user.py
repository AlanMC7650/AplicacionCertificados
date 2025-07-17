from app.extensions import db


class Usuario(db.Model):
    """docstring for Usuario"""

    __tablename__ = "usuarios"

    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    contrasena = db.Column(db.String(200), nullable=False)
    documento = db.Column(db.String(30), nullable=False)
    pais_origen = db.Column(db.String(50), nullable=False)
