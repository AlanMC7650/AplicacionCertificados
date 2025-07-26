import psycopg2
from app.db_c import get_connection


def obtener_cursos():
    conn = get_connection()  # conecta a la base de datos
    cursor = conn.cursor()  # crea un cursor (como el "puente" para hacer consultas)
    cursor.execute("SELECT * FROM cursos")  # consulta SQL directa
    rows = cursor.fetchall()  # obtiene todos los resultados en una lista
    conn.close()  # cierra la conexión
    return rows  # devuelve los datos a quien haya llamado esta función


def obtener_curso(id_curso):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cursos WHERE id_curso = %s", (id_curso,))
    row = cursor.fetchone()
    conn.close()
    return row


def crear_curso(nombre, descripcion, modalidad, id_version, id_ponente):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO cursos (nombre, descripcion, modalidad, id_version, id_ponente) VALUES (%s,%s,%s,%s,%s)",
        (
            nombre,
            descripcion,
            modalidad,
            id_version,
            id_ponente,
        ),
    )
    conn.commit()
    conn.close()


def actualizar_curso(id_curso, nombre, descripcion, modalidad, id_version, id_ponente):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE cursos SET nombre = %s, descripcion = %s, modalidad = %s, id_version = %s, id_ponente = %s WHERE id_curso = %s",
        (
            nombre,
            descripcion,
            modalidad,
            id_version,
            id_ponente,
            id_curso,
        ),
    )
    conn.commit()
    conn.close()


def eliminar_curso(id_curso):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cursos WHERE id_curso = %s", (id_curso,))
        conn.commit()
        conn.close()
    except psycopg2.Error as e:
        conn.rollback()
        return {"status": "error", "mensaje": "Error al eliminar: " + str(e)}
