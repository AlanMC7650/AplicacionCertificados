from flask import render_template, request, redirect, url_for, flash, session
import json
from werkzeug.utils import secure_filename
import pandas as pd
import os
import io

from . import rxls_bp
from app import db
from app.models.user import Usuario

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@rxls_bp.route("/", methods=["GET", "POST"])
def index():
    tabla_html = None

    if request.method == "POST":
        accion = request.form.get("accion")

        if accion == "vista":
            file = request.files.get("file")
            if not file:
                flash("No se recibió archivo.")
                return redirect(request.url)

            ext = file.filename.rsplit('.', 1)[1].lower()
            df = pd.read_csv(file) if ext == 'csv' else pd.read_excel(file)
            session["datos_usuarios"] = df.to_json()  # Guardamos en sesión
            tabla_html = df.to_html(classes="table table-bordered", index=False, border=0)
            flash("Archivo leído correctamente.")

        elif accion == "guardar":
            try:
                json_str = session.get("datos_usuarios")
                if not json_str:
                    flash("No hay datos para guardar.")
                    return redirect(request.url)
                df = pd.read_json(io.StringIO(json_str))
                for _, row in df.iterrows():
                    usuario = Usuario(
                        nombre=row['nombre'],
                        apellido=row['apellido'],
                        email=row['email'],
                        contrasena=row['contrasena'],
                        documento=row['documento'],
                        pais_origen=row['pais_origen']
                    )
                    db.session.add(usuario)
                db.session.commit()
                session.pop("datos_usuarios", None)
                flash("Datos guardados exitosamente.")
                return redirect(url_for("rxls_bp.index"))

            except Exception as e:
                flash(f"Error al guardar: {e}")

    return render_template("readxls/readxls.html", tabla=tabla_html)