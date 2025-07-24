from flask import Blueprint, render_template
from app.api.coordinador import coordinador_bp
from flask_login import login_user, logout_user, login_required, current_user


@coordinador_bp.route("/")
@login_required
def index():
    return render_template("Coordinador/indexCoordinador.html")


@coordinador_bp.route("/estudiantes", methods=["GET"])
@login_required
def estudiantes():
    lista_estudiantes = [
        {
            "id": 1,
            "nombre": "Juan",
            "apellido": "Pérez",
            "certificado": "Sí",
            "ci": "12345678",
            "nota": 90,
        },
        {
            "id": 2,
            "nombre": "María",
            "apellido": "Gómez",
            "certificado": "No",
            "ci": "87654321",
            "nota": 85,
        },
    ]
    return render_template(
        "Coordinador/partials/estudiantes.html", estudiantes=lista_estudiantes
    )


@coordinador_bp.route("/expositores")
@login_required
def expositores():
    return render_template("Coordinador/partials/expositores.html")


@coordinador_bp.route("/cursos")
@login_required
def cursos():
    return render_template("Coordinador/partials/cursos.html")


@coordinador_bp.route("/eventos")
@login_required
def eventos():
    return render_template("Coordinador/partials/eventos.html")
