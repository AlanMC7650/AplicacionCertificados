from sqlalchemy import Column, Integer, String
from app.db import Base  # Asegúrate de tener esta base desde tu SQLAlchemy setup


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    contrasena = Column(String(200), nullable=False)
    documento = Column(String(30), nullable=False)
    pais_origen = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<Usuario {self.nombre} {self.apellido} - {self.email}>"
