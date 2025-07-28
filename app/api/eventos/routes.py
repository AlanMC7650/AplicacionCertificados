from flask import Blueprint, request, jsonify, render_template
from . import evento_bp
from app.controllers import e_controller as evt
from flask_login import login_user, logout_user, login_required, current_user
from app.api.auth.utils import role_required



@evento_bp.route("/eventos", methods=["GET"])
@login_required
def eventos():
    return render_template("Coordinador/partials/eventos.html", eventos=evt.obtener_eventos())


# @evento_bp.route("/", methods=["GET"])
# @login_required
# def get_eventos():
#     try:
#         datos = evt.obtener_eventos()
#         eventos = []
#         for row in datos:
#             eventos.append({"id_evento": row[0], "nombre_base": row[1]})
#         return jsonify(eventos)
#     except Exception as e:
#         print("Error al obtener eventos:", e)
#         return (
#             jsonify({"error": str(e)}),
#             500,
#         )  # cambié el [] que seria una coleccion vacia


@evento_bp.route("/<int:id_evento>", methods=["GET"])
@login_required
def get_evento(id_evento):
    row = evt.obtener_evento(id_evento)
    if row:
        evento = {"id_evento": row[0], "nombre_base": row[1]}
        return jsonify(evento)
    return jsonify({"mensaje": "Evento no encontrado"}), 404


@evento_bp.route("/", methods=["POST"])
@login_required
def post_evento():
    data = request.json
    evt.crear_evento(data["nombre_base"])
    return jsonify({"mensaje": "Evento creado"}), 201


@evento_bp.route("/<int:id_evento>", methods=["PUT"])
@login_required
def put_evento(id_evento):
    data = request.json
    evt.actualizar_evento(id_evento, data["nombre_base"])
    return jsonify({"mensaje": "Evento actualizado"})


@evento_bp.route("/<int:id_evento>", methods=["DELETE"])
@login_required
def delete_evento(id_evento):
    evt.eliminar_evento(id_evento)
    return jsonify({"mensaje": "Evento eliminado"})


# version evento


@evento_bp.route("/version", methods=["GET"])
@login_required
def get_eventosVs():
    try:
        datos = evt.obtener_eventosVs()
        eventosVs = []
        for row in datos:
            eventosVs.append(
                {
                    "id_version": row[0],
                    "id_evento": row[1],
                    "nombre_version": row[2],
                    "anio": row[3],
                    "fecha_inicio": row[4],
                    "fecha_fin": row[5],
                    "lugar": row[6],
                }
            )
        return jsonify(eventosVs)
    except Exception as e:
        print("Error al obtener las versiones de eventos:", e)
        return (
            jsonify({"error": str(e)}),
            500,
        )  # cambié el [] que seria una coleccion vacia


@evento_bp.route("/version/<int:id_version>", methods=["GET"])
@login_required
def get_eventoVs(id_version):
    row = evt.obtener_eventoVs(id_version)
    if row:
        eventoVs = {
            "id_version": row[0],
            "id_evento": row[1],
            "nombre_version": row[2],
            "anio": row[3],
            "fecha_inicio": row[4],
            "fecha_fin": row[5],
            "lugar": row[6],
        }
        return jsonify(eventoVs)
    return jsonify({"mensaje": "Version de evento no encontrado"}), 404


@evento_bp.route("/version", methods=["POST"])
@login_required
def post_eventoVs():
    data = request.json
    evt.crear_eventoVs(
        data["id_evento"],
        data["nombre_version"],
        data["anio"],
        data["fecha_inicio"],
        data["fecha_fin"],
        data["lugar"],
    )
    return jsonify({"mensaje": "Version de evento creado"}), 201


@evento_bp.route("/version/<int:id_version>", methods=["PUT"])
@login_required
def put_eventoVs(id_version):
    data = request.json
    evt.actualizar_eventoVs(
        data["id_evento"],
        data["nombre_version"],
        data["anio"],
        data["fecha_inicio"],
        data["fecha_fin"],
        data["lugar"],
        id_version,
    )

    return jsonify({"mensaje": "Version de evento actualizado"})


@evento_bp.route("/version/<int:id_version>", methods=["DELETE"])
@login_required
def delete_eventoVs(id_version):
    evt.eliminar_eventoVs(id_version)
    return jsonify({"mensaje": "Version de evento eliminado"})
