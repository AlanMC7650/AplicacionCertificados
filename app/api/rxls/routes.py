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
    if request.method == "POST":
        if 'file' not in request.files:
            flash('No se ha enviado ningún archivo.')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('Nombre de archivo vacío.')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file.save(filepath)

            # Leer y subir a la base de datos
            df = pd.read_excel(filepath)
            for _, row in df.iterrows():
                usuario = Usuario(
                    nombre=row['nombre'], apellido=row['apellido'], 
                    email=row['email'], contrasena=row['contrasena'],
                    documento=row['documento'], pais_origen=row['pais_origen']
                    )
                db.session.add(usuario)
            db.session.commit()

            flash("Archivo cargado y datos insertados correctamente.")
            return redirect(url_for('main.index'))

    return render_template("readxls/readxls.html")
