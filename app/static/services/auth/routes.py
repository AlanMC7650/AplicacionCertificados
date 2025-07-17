# Importamos las librerias de flask necesarias para renderizar los templates html
from flask import render_template, request, redirect, url_for, flash, session

# Seguridad de las contraseñas y comparar las mismas
from werkzeug.security import check_password_hash

# Traemos el blueprint creado en __init__.py
from . import auth_bp

# Importamos el modelo usuario de SQLAlchemy
from app.models.user import db, Usuario


# Creamos la ruta a la debe dirigirnos el blueprint
@auth_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        contrasena = request.form["contrasena"]

        print(f"Email recibido: {email}")
        print(f"Contraseña recibida: {contrasena}")

        user = Usuario.query.filter_by(email=email).first()
        print(f"Usuario encontrado: {user}")
        print(user and check_password_hash(user.contrasena, contrasena))
        if user and check_password_hash(user.contrasena, contrasena):
            print("Contrasena correcta")
            session["user_id"] = user.id_usuario
            session["nombre"] = user.nombre
            flash("Inicio de sesión exitoso", "success")
            return redirect(
                url_for("auth.dashboard")
            )  # o el nombre correcto del endpoint dashboard
        else:
            flash("Credenciales incorrectas", "danger")

    return render_template("login.html")


@auth_bp.route("/dashboard", methods=["GET"])
def dashboard():
    if "user_id" in session:
        return render_template(
            "dashboard.html", nombre="DIEGO ANDRÉS FLORES GUTIERREZ"
        )  # // ya que no hay base de datos aqui insertamos el nombre del estudiante a mostrar en la vista de dashboard
    return "Acceso denegado"
