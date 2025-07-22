from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import pandas as pd
import os

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
    df = None

    if request.method == "POST":
        accion = request.form.get("accion")

        if 'file' not in request.files:
            flash('No se ha enviado ningún archivo.')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('Nombre de archivo vacío.')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            ext = file.filename.rsplit('.', 1)[1].lower()

            try:
                if ext == 'csv':
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)

                if accion == 'vista':
                    # Solo mostrar la tabla
                    tabla_html = df.to_html(classes="table table-bordered", index=False, border=0)
                    flash("Archivo leído correctamente. Revisa la vista previa.")
                
                elif accion == 'guardar':
                    # Guardar en base de datos
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
                    flash("Datos guardados en la base de datos.")
                    return redirect(url_for('rxls_bp.index'))  # recargar la página limpia

            except Exception as e:
                flash(f"Error al procesar el archivo: {e}")

    return render_template("readxls/readxls.html", tabla=tabla_html)
