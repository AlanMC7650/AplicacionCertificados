from flask import render_template, request, redirect, url_for, flash, session
import pandas as pd
import io

from . import rxls_bp
from app import db
from app.models.user import Usuario
from flask_login import login_required
from .controller import crear_estudiantes_bulk

ALLOWED_EXTENSIONS = {"xlsx", "xls", "csv"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@rxls_bp.route("/", methods=["GET", "POST"])
@login_required
def index():
    tabla_html = None

    if request.method == "POST":
        accion = request.form.get("accion")

        if accion == "vista":
            file = request.files.get("file")

            if not file or not allowed_file(file.filename):
                flash("Archivo no válido o no recibido.")
                return redirect(request.url)

            try:
                ext = file.filename.rsplit(".", 1)[1].lower()
                df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)
                df.columns = df.columns.str.strip().str.lower()
                session["df_data"] = df.to_json()
                tabla_html = df.to_html(
                    classes="table table-bordered", index=False, border=0
                )
                flash("Archivo leído correctamente.")
                return render_template("readxls/readxls.html", tabla=tabla_html)
            except Exception as e:
                flash(f"Error al procesar el archivo: {e}")
                return redirect(request.url)

        elif accion == "guardar":
            try:
                if "df_data" not in session:
                    flash("No hay datos para guardar.")
                    return redirect(request.url)

                df = pd.read_json(io.StringIO(session["df_data"]))
                insertados = df.to_dict(orient="records")
                crear_estudiantes_bulk(insertados)

                session.pop("df_data", None)
                flash(f"{len(insertados)} estudiantes guardados correctamente.")
                return redirect(url_for("rxls_bp.index"))
            except Exception as e:
                flash(f"Error al guardar estudiantes: {e}")
                return redirect(request.url)

    return render_template("readxls/readxls.html", tabla=tabla_html)
