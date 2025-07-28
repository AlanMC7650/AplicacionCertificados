from flask import Blueprint, request, jsonify, render_template
from . import curso_bp
from app.controllers import c_controller as crs
from flask_login import login_user, logout_user, login_required, current_user


@curso_bp.route("/cursos", methods=["GET"])
@login_required
def cursos():
    return render_template("Coordinador/partials/cursos.html", cursos=crs.obtener_cursos())


# @curso_bp.route("/", methods=["GET"])
# @login_required
# def get_cursos():
#     try:
#         datos = crs.obtener_cursos()
#         cursos = []
#         for row in datos:
#             cursos.append(
#                 {
#                     "id_curso": row[0],
#                     "nombre": row[1],
#                     "descripcion": row[2],
#                     "modalidad": row[3],
#                     "id_version": row[4],
#                     "id_ponente": row[5],
#                 }
#             )
#         return jsonify(cursos)
#     except Exception as e:
#         print("Error al obtener cursos:", e)
#         return (
#             jsonify({"error": str(e)}),
#             500,
#         )  # cambié el [] que seria una coleccion vacia


@curso_bp.route("/<int:id_curso>", methods=["GET"])
@login_required
def get_curso(id_curso):
    row = crs.obtener_curso(id_curso)
    if row:
        curso = {
            "id_curso": row[0],
            "nombre": row[1],
            "descripcion": row[2],
            "modalidad": row[3],
            "id_version": row[4],
            "id_ponente": row[5],
        }
        return jsonify(curso)
    return jsonify({"mensaje": "Curso no encontrado"}), 404


@curso_bp.route("/", methods=["POST"])
@login_required
def post_curso():
    data = request.json
    crs.crear_curso(
        data["nombre"],
        data["descripcion"],
        data["modalidad"],
        data["id_version"],
        data["id_ponente"],
    )
    return jsonify({"mensaje": "Curso creado"}), 201


@curso_bp.route("/<int:id_curso>", methods=["PUT"])
@login_required
def put_curso(id_curso):
    data = request.json
    crs.actualizar_curso(
        id_curso,
        data["nombre"],
        data["descripcion"],
        data["modalidad"],
        data["id_version"],
        data["id_ponente"],
    )
    return jsonify({"mensaje": "Curso actualizado"})


@curso_bp.route("/<int:id_curso>", methods=["DELETE"])
@login_required
def delete_curso(id_curso):
    crs.eliminar_curso(id_curso)
    return jsonify({"mensaje": "Curso eliminado"})


"""
TIENE UN PROBLEMA CON EL DELETE POR UNA RESTRICCION EN LA BD, ARREGLAR ESO, TAMBIEN EN EL CRUD DE USUARIOS
"""
