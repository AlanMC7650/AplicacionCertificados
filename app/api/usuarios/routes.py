from flask import Blueprint, request, jsonify, render_template
from . import usuario_bp
from . import controller as est
@usuario_bp.route('/estudiantes', methods=['GET'])
def get_estudiantes():
    try:
        datos = est.obtener_estudiantes()
        estudiantes = []
        for row in datos:
            estudiantes.append({
                "id_usuario": row[0],
                "nombre": row[1],
                "apellido": row[2],
                "email": row[3],
                "contrasena": row[4],
                "documento": row[5],
                "pais_origen": row[6],
                "id_rol": row[7]
            })
        return jsonify(estudiantes)
    except Exception as e:
        print("Error al obtener estudiantes:", e)
        return jsonify({"error": str(e)}), 500 #cambié el [] que seria una coleccion vacia


@usuario_bp.route('/estudiantes/<int:id_usuario>', methods=['GET'])
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
                "id_rol": row[7]
        }
        return jsonify(estudiante)
    return jsonify({"mensaje": "Estudiante no encontrado"}), 404


'''@usuario_bp.route('/estudiantes', methods=['POST'])
def post_estudiante():
    data = request.json
    est.crear_estudiante(data['nombre'], data['apellido'], data['email'], data['contrasena'], data['documento'], data['pais_origen'])
    return jsonify({"mensaje": "Estudiante creado"}), 201'''

@usuario_bp.route('/estudiantes', methods=['POST'])
def post_estudiante():
    data = request.json
    est.crear_estudiante(
        data['nombre'], data['apellido'], data['email'],
        data['contrasena'], data['documento'], data['pais_origen'],
        data['id_rol']
    )
    return jsonify({"mensaje": "Estudiante creado"}), 201

'''@usuario_bp.route('/estudiantes/<int:id_usuario>', methods=['PUT'])
def put_estudiante(id_usuario):
    data = request.json
    est.actualizar_estudiante(id_usuario, data['nombre'], data['apellido'], data['email'], data['contrasena'], data['documento'], data['pais_origen'])
    return jsonify({"mensaje": "Estudiante actualizado"})
'''

@usuario_bp.route('/estudiantes/<int:id_usuario>', methods=['PUT'])
def put_estudiante(id_usuario):
    data = request.json
    est.actualizar_estudiante(
        id_usuario,
        data['nombre'], data['apellido'], data['email'],
        data['contrasena'], data['documento'], data['pais_origen'],
        data['id_rol']
    )
    return jsonify({"mensaje": "Estudiante actualizado"})

@usuario_bp.route('/estudiantes/<int:id_usuario>', methods=['DELETE'])
def delete_estudiante(id_usuario):
    est.eliminar_estudiante(id_usuario)
    return jsonify({"mensaje": "Estudiante eliminado"})
