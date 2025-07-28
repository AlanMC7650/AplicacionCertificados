from flask import render_template
from app.api.ponente import ponente_bp
from flask_login import login_required, current_user
from app.api.auth.utils import role_required


@ponente_bp.route("/")
@login_required
def index():
    return render_template(
        "Expositor/expositor.html",
        nombre=current_user.nombre,
        apellido=current_user.apellido,
    )


@ponente_bp.route("/datos")
@login_required
def datos():
    return render_template(
        "Expositor/datosPersonalesExp.html",
        nombre=current_user.nombre,
        apellido=current_user.apellido,
        email=current_user.email,
        documento=current_user.documento,
        pais_origen=current_user.pais_origen,
    )


@ponente_bp.route("/curso")
@login_required
def curso():
    return render_template("Expositor/CursoExp.html")


@ponente_bp.route("/calificacion")
@login_required
def calificacion():
    return render_template("Expositor/calificacionExp.html")
