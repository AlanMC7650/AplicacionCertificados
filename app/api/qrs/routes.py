import os
import segno
from flask import Blueprint, request, jsonify, send_from_directory
from datetime import datetime
from . import qrs_bp

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../static/qrs"))


@qrs_bp.route("/<path:filename>", methods=["GET"])
def serve_qr(filename):
    return send_from_directory(BASE_DIR, filename)


@qrs_bp.route("/generate_qr", methods=["POST"])
def generate_qr():
    data = request.json.get("url")
    if not data:
        return jsonify({"error": "No se proporcionó ningún enlace"}), 400

    try:
        qr = segno.make(data)
        os.makedirs(BASE_DIR, exist_ok=True)

        filename = f"qr_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        output_file = os.path.join(BASE_DIR, filename)
        qr.save(output_file, scale=10)

        return jsonify({"message": "QR generado con éxito", "filename": filename}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
