import os
import segno
from flask import (
    Blueprint,
    request,
    jsonify,
    send_from_directory,
    render_template,
    redirect,
    url_for,
)
from datetime import datetime
from . import qrs_bp
from app.controllers import u_controller as est  # Importa el controlador de estudiantes
from flask_login import login_user, logout_user, login_required, current_user
from app.api.auth.utils import role_required

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../static/qrs"))

@qrs_bp.route("/<path:filename>", methods=["GET"])
@login_required
def serve_qr(filename):
    return send_from_directory(BASE_DIR, filename)

@qrs_bp.route("/generate_qr/<int:id_usuario>", methods=["GET"])
@login_required
def generate_qr_by_id(id_usuario):
    try:
        row = est.obtener_estudiante(id_usuario)
        if not row:
            return jsonify({"error": "Estudiante no encontrado"}), 404

        # Verificar si ya existe un QR para este id_usuario
        existing_files = [
            fname
            for fname in os.listdir(BASE_DIR)
            if fname.startswith(f"qr_{id_usuario}_") and fname.endswith(".png")
        ]

        if existing_files:
            # Si hay un QR ya generado, devolver ese
            existing_filename = existing_files[0]
            return (
                jsonify(
                    {
                        "message": "Ya existe un QR generado para este usuario.",
                        "filename": existing_filename,
                        "path": f"/qrs/{existing_filename}",
                    }
                ),
                200,
            )

        # Generar nuevo QR
        contenido = f"ID: {row[0]}"
        qr = segno.make(contenido)
        os.makedirs(BASE_DIR, exist_ok=True)

        filename = f"qr_{id_usuario}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        output_file = os.path.join(BASE_DIR, filename)
        qr.save(output_file, scale=30)

        return redirect(url_for("qrs.perfil_estudiante", id_usuario=id_usuario))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@qrs_bp.route("/perfil_estudiante/<int:id_usuario>", methods=["GET"])
@login_required
def perfil_estudiante(id_usuario):
    try:
        row = est.obtener_estudiante(id_usuario)
        if not row:
            return "Estudiante no encontrado", 404

        # Buscar QR existente
        qr_filename = None
        for fname in os.listdir(BASE_DIR):
            if fname.startswith(f"qr_{id_usuario}_") and fname.endswith(".png"):
                qr_filename = fname
                break

        # Si no hay QR, podrías generarlo automáticamente o simplemente no mostrarlo
        qr_path = f"/qrs/{qr_filename}" if qr_filename else None

        return render_template(
            "Estudiante/Estudiante.html",  # Reemplaza con la ruta real de tu template
            estudiante=row,
            qr_path=qr_path,
        )

    except Exception as e:
        return str(e), 500
