from flask import (
    render_template,
    send_file,
    current_app,
    request,
    flash,
    redirect,
    url_for,
)
from flask_mail import Mail, Message
from sqlalchemy import text
from app import db, mail
from . import certificate_bp
from fpdf import FPDF
from datetime import datetime
import pandas as pd
import os, shutil, zipfile
from flask_login import login_user, logout_user, login_required, current_user
from app.api.auth.utils import role_required


@certificate_bp.route("/generar-certificados")
@login_required
@role_required(1, 4)
def generar_certificados():
    folder = "temp_certificates"
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)

    # Leer datos
    with db.engine.connect() as conn:
        query = """ SELECT 
                        u.nombre as student, 
                        u.apellido as apellido                         
                    FROM 
                        usuarios u"""
        result = conn.execute(text(query))
        participants = pd.DataFrame(result.fetchall(), columns=result.keys())

    for _, row in participants.iterrows():
        student = row["student"]
        apellido = row["apellido"]
        # course = row['course']
        # date = row['date']
        date = "2025-10-20"

        pdf = FPDF(orientation="L", unit="pt", format="A4")
        pdf.add_page()
        template_path = os.path.join(
            os.path.dirname(__file__), "input", "certificate_template.jpg"
        )
        pdf.image(template_path, 0, 0, w=842, h=595)

        pdf.set_font("Helvetica", "B", 50)
        pdf.set_text_color(139, 119, 40)
        pdf.set_xy(0, 230)
        pdf.cell(w=842, h=60, txt=student, align="C")

        pdf.set_font("Helvetica", "", 25)
        pdf.set_xy(0, 360)
        pdf.cell(w=842, h=30, txt=apellido, align="C")

        pdf.set_font("Helvetica", "I", 16)
        pdf.set_text_color(1, 1, 1)
        pdf.set_xy(155, 500)
        pdf.cell(w=842, h=20, txt=str(date), align="C")

        file_name = student.replace(" ", "_") + apellido.replace(" ", "_")
        pdf.output(f"{folder}/{file_name}_certificate.pdf")

    zip_name = f"certificados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    zip_path = f"{folder}/{zip_name}"
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith(".pdf"):
                    zipf.write(os.path.join(root, file), arcname=file)

    return send_file(zip_path, as_attachment=True)


@certificate_bp.route("/enviar-certificado/<int:user_id>", methods=["GET", "POST"])
@login_required
@role_required(1, 4)
def enviar_certificado(user_id):
    # Leer los datos del usuario
    with db.engine.connect() as conn:
        query = text(
            "SELECT nombre, apellido, email FROM usuarios WHERE id_usuario = :id"
        )
        result = conn.execute(query, {"id": user_id}).fetchone()

        if not result:
            return "Usuario no encontrado", 404

        # Acceso correcto por índice
        student, apellido, email = result[0], result[1], result[2]

    if request.method == "POST":
        asunto = request.form["asunto"]
        mensaje = request.form["mensaje"]

        # Crear el certificado en memoria
        pdf = FPDF(orientation="L", unit="pt", format="A4")
        pdf.add_page()
        template_path = os.path.join(
            os.path.dirname(__file__), "input", "certificate_template.jpg"
        )
        pdf.image(template_path, 0, 0, w=842, h=595)

        pdf.set_font("Helvetica", "B", 50)
        pdf.set_text_color(139, 119, 40)
        pdf.set_xy(0, 230)
        pdf.cell(w=842, h=60, txt=student, align="C")

        pdf.set_font("Helvetica", "", 25)
        pdf.set_xy(0, 360)
        pdf.cell(w=842, h=30, txt=apellido, align="C")

        pdf.set_font("Helvetica", "I", 16)
        pdf.set_text_color(1, 1, 1)
        pdf.set_xy(155, 500)
        pdf.cell(w=842, h=20, txt="2025-10-20", align="C")

        # Guardar temporalmente
        file_name = (
            f"{student.replace(' ', '_')}_{apellido.replace(' ', '_')}_certificate.pdf"
        )
        output_path = os.path.join("temp_certificates", file_name)
        os.makedirs("temp_certificates", exist_ok=True)
        pdf.output(output_path)

        # Enviar correo
        msg = Message(asunto, sender=os.getenv("MAIL_USERNAME"), recipients=[email])
        msg.body = mensaje
        with open(output_path, "rb") as f:
            msg.attach(
                filename=file_name, content_type="application/pdf", data=f.read()
            )
        mail.send(msg)

        flash(f"Certificado enviado a {email}", "success")
        return redirect(url_for("certificate.enviar_certificado", user_id=user_id))

    return render_template(
        "send_certificate.html", student=student, apellido=apellido, email=email
    )


@certificate_bp.route("/enviar-certificados-todos", methods=["GET", "POST"])
@login_required
@role_required(1, 4)
def enviar_certificados_todos():
    if request.method == "POST":
        asunto = request.form.get("asunto")
        mensaje = request.form.get("mensaje")

        with db.engine.connect() as conn:
            query = text(
                "SELECT id_usuario, nombre, apellido, email FROM usuarios WHERE id_usuario=4 OR id_usuario=6"
            )
            usuarios = conn.execute(query).fetchall()

        errores_envio = []
        exitos_envio = []
        os.makedirs("temp_certificates", exist_ok=True)

        for user in usuarios:
            user_id, student, apellido, email = user

            # Generar PDF
            pdf = FPDF(orientation="L", unit="pt", format="A4")
            pdf.add_page()
            template_path = os.path.join(
                os.path.dirname(__file__), "input", "certificate_template.jpg"
            )
            pdf.image(template_path, 0, 0, w=842, h=595)

            pdf.set_font("Helvetica", "B", 50)
            pdf.set_text_color(139, 119, 40)
            pdf.set_xy(0, 230)
            pdf.cell(w=842, h=60, txt=student, align="C")

            pdf.set_font("Helvetica", "", 25)
            pdf.set_xy(0, 360)
            pdf.cell(w=842, h=30, txt=apellido, align="C")

            pdf.set_font("Helvetica", "I", 16)
            pdf.set_text_color(1, 1, 1)
            pdf.set_xy(155, 500)
            pdf.cell(w=842, h=20, txt="2025-10-20", align="C")

            file_name = f"{student.replace(' ', '_')}_{apellido.replace(' ', '_')}_certificate.pdf"
            output_path = os.path.join("temp_certificates", file_name)
            pdf.output(output_path)

            # Enviar correo
            msg = Message(
                subject=asunto, sender=os.getenv("MAIL_USERNAME"), recipients=[email]
            )
            msg.body = mensaje

            try:
                with open(output_path, "rb") as f:
                    msg.attach(
                        filename=file_name,
                        content_type="application/pdf",
                        data=f.read(),
                    )
                mail.send(msg)
                exitos_envio.append(email)
            except Exception as e:
                errores_envio.append((email, str(e)))

        shutil.rmtree("temp_certificates")

        flash(f"Certificados enviados a {len(exitos_envio)} usuarios.", "success")
        if errores_envio:
            flash(
                f"Errores al enviar a: {', '.join(e[0] for e in errores_envio)}",
                "error",
            )

        return redirect(url_for("certificate.enviar_certificados_todos"))

    # GET: mostrar formulario con valores por defecto
    return render_template("send_bulk_certificate.html")
