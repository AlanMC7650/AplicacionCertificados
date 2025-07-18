# Importamos las librerias de flask necesarias para renderizar los templates html
from flask import render_template, request, redirect, url_for, flash, session

# Seguridad de las contraseñas y comparar las mismas
from werkzeug.security import check_password_hash, generate_password_hash

# Traemos el blueprint creado en __init__.py
from . import auth_bp

# Importamos el modelo usuario de SQLAlchemy
from app.models.user import db, Usuario

# Importamos los formularios generados por python
from .forms import ForgotPasswordForm, ResetPasswordForm

# Impotamos las funciones útiles para forgot my password
from .utils import send_reset_email, verify_reset_token

# Importamos librerias para trabajar con el login
from flask_login import login_user, logout_user, login_required, current_user


# Creamos la ruta a la debe dirigirnos el blueprint
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))

    if request.method == "POST":
        email = request.form["email"]
        contrasena = request.form["contrasena"]
        recuerdame = request.form.get("recuerdame") == "on"

        user = Usuario.query.filter_by(email=email).first()

        if user and check_password_hash(user.contrasena, contrasena):
            login_user(user, remember=recuerdame)
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for("auth.dashboard"))
        else:
            flash("Usuario y/o contraseña invalidos", "danger")

    return render_template("login.html")


@auth_bp.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    return render_template("dashboard.html", nombre=current_user.nombre)


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
        flash(
            "Si el correo existe, se enviará un enlace para restablecer la contraseña.",
            "info",
        )
        return redirect(url_for("auth.forgot_password"))
    return render_template("forgot_password.html", form=form)


@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_token(token):
    email = verify_reset_token(token)
    if not email:
        flash("El enlace es inválido o ha expirado.", "danger")
        return redirect(url_for("auth.forgot_password"))

    user = Usuario.query.filter_by(email=email).first_or_404()
    form = ResetPasswordForm()

    if form.validate_on_submit():
        user.contrasena = generate_password_hash(form.password.data)
        db.session.commit()
        flash("¡Tu contraseña ha sido actualizada!", "success")
        return redirect(url_for("auth.login"))

    return render_template("reset_password.html", form=form)


@auth_bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión exitosamente.", "info")
    return redirect(url_for("auth.login"))
