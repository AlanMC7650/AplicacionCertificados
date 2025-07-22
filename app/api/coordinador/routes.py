from flask import Blueprint, render_template
from app.api.coordinador import coordinador_bp

@coordinador_bp.route('/')
def index():
    return render_template('Coordinador/indexCoordinador.html')

@coordinador_bp.route('/estudiantes')
def estudiantes():
    lista_estudiantes = [
        {'id': 1, 'nombre': 'Juan', 'apellido': 'Pérez', 'certificado': 'Sí', 'ci': '12345678', 'nota': 90},
        {'id': 2, 'nombre': 'María', 'apellido': 'Gómez', 'certificado': 'No', 'ci': '87654321', 'nota': 85},
    ]
    return render_template('Coordinador/partials/estudiantes.html', estudiantes=lista_estudiantes)

@coordinador_bp.route('/expositores')
def expositores():
    return render_template('Coordinador/partials/expositores.html')

@coordinador_bp.route('/cursos')
def cursos():
    return render_template('Coordinador/partials/cursos.html')

@coordinador_bp.route('/eventos')
def eventos():
    return render_template('Coordinador/partials/eventos.html')
