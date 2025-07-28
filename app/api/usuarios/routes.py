from flask import Blueprint, request, jsonify, render_template
from . import usuario_bp
from app.controllers import u_controller as usu
from app.controllers import u_controller as est
from flask_login import login_user, logout_user, login_required, current_user



# --- PARA COORDINADOR ---
## Estudiantes
@usuario_bp.route("/coor/estudiantes", methods=["POST"])
@login_required
def post_estudiante():
    data = request.json
    usu.crear_estudiante(
        data["nombre"],
        data["apellido"],
        data["email"],
        data["contrasena"],
        data["documento"],
        data["pais_origen"],
        data["id_rol"],
    )
    return jsonify({"mensaje": "Estudiante creado"}), 201

@usuario_bp.route("coor/estudiantes", methods=["GET"])
@login_required
def obtener_estudiantes():
    return render_template("Coordinador/partials/estudiantes.html", estudiantes=usu.obtener_usuarios(rol=3))

@usuario_bp.route("/coor/estudiantes/<int:id_usuario>", methods=["PUT"])
@login_required
def editar_estudiante(id_usuario):
    data = request.json
    est.actualizar_estudiante(
        id_usuario,
        data["nombre"],
        data["apellido"],
        data["email"],
        data["contrasena"],
        data["documento"],
        data["pais_origen"],
        data["id_rol"],
    )
    return jsonify({"mensaje": "Estudiante actualizado"})

@usuario_bp.route("/coor/estudiantes/<int:id_usuario>", methods=["DELETE"])
@login_required
def borrar_estudiante(id_usuario):
    usu.eliminar_estudiante(id_usuario)
    return jsonify({"mensaje": "Estudiante eliminado"})



## Ponentes
@usuario_bp.route("coor/expositores", methods=["GET"])
@login_required
def expositores():
    return render_template("Coordinador/partials/expositores.html",expositores=est.obtener_usuarios(2))


# --- DEMAS ---

@usuario_bp.route("/estudiantes/<int:id_usuario>", methods=["PUT"])
@login_required
def put_estudiante(id_usuario):
    data = request.json
    est.actualizar_estudiante(
        id_usuario,
        data["nombre"],
        data["apellido"],
        data["email"],
        data["contrasena"],
        data["documento"],
        data["pais_origen"],
        data["id_rol"],
    )
    return jsonify({"mensaje": "Estudiante actualizado"})

@usuario_bp.route("/estudiantes/<int:id_usuario>", methods=["GET"])
@login_required
def get_estudiante(id_usuario):
    row = est.obtener_estudiante(id_usuario)
    if row:
        estudiante = {
            "id_usuario": row[0],
            "nombre": row[1],
            "apellido": row[2],
            "email": row[3],
            "contrasena": row[4],
            "documento": row[5],
            "pais_origen": row[6],
            "id_rol": row[7],
        }
        return jsonify(estudiante)
    return jsonify({"mensaje": "Estudiante no encontrado"}), 404


"""@usuario_bp.route('/estudiantes', methods=['POST'])
def post_estudiante():
    data = request.json
    est.crear_estudiante(data['nombre'], data['apellido'], data['email'], data['contrasena'], data['documento'], data['pais_origen'])
    return jsonify({"mensaje": "Estudiante creado"}), 201"""


# @usuario_bp.route("/estudiantes", methods=["POST"])
# @login_required
# def post_estudiante():
#     data = request.json
#     est.crear_estudiante(
#         data["nombre"],
#         data["apellido"],
#         data["email"],
#         data["contrasena"],
#         data["documento"],
#         data["pais_origen"],
#         data["id_rol"],
#     )
#     return jsonify({"mensaje": "Estudiante creado"}), 201


"""@usuario_bp.route('/estudiantes/<int:id_usuario>', methods=['PUT'])
def put_estudiante(id_usuario):
    data = request.json
    est.actualizar_estudiante(id_usuario, data['nombre'], data['apellido'], data['email'], data['contrasena'], data['documento'], data['pais_origen'])
    return jsonify({"mensaje": "Estudiante actualizado"})
"""


# @usuario_bp.route("/estudiantes/<int:id_usuario>", methods=["PUT"])
# @login_required
# def put_estudiante(id_usuario):
#     data = request.json
#     est.actualizar_estudiante(
#         id_usuario,
#         data["nombre"],
#         data["apellido"],
#         data["email"],
#         data["contrasena"],
#         data["documento"],
#         data["pais_origen"],
#         data["id_rol"],
#     )
#     return jsonify({"mensaje": "Estudiante actualizado"})