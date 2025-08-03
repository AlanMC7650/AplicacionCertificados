import psycopg2
from app.db_c import get_connection
from werkzeug.security import generate_password_hash


# --- Usuarios General
def obtener_usuarios(rol):
    conn = get_connection()  # conecta a la base de datos
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(
        "SELECT * FROM Usuarios WHERE id_rol = %s", (rol,)
    )  # consulta SQL directa
    rows = cursor.fetchall()  # obtiene todos los resultados en una lista
    conn.close()  # cierra la conexión
    return rows  # devuelve los datos a quien haya llamado esta función


def obtener_usuarios_id(rol, id):
    conn = get_connection()  # conecta a la base de datos
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(
        "SELECT * FROM Usuarios WHERE id_rol = %s and id_usuario=%s", (rol, id)
    )  # consulta SQL directa
    rows = cursor.fetchall()  # obtiene todos los resultados en una lista
    conn.close()  # cierra la conexión
    return rows  # devuelve los datos a quien haya llamado esta función


# --- Usuarios Estudiantes
def obtener_estudiantes():
    conn = get_connection()  # conecta a la base de datos
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM Usuarios WHERE id_rol = 3 ORDER BY id_usuario ASC;")  # consulta SQL directa
    rows = cursor.fetchall()  # obtiene todos los resultados en una lista
    conn.close()  # cierra la conexión
    return rows  # devuelve los datos a quien haya llamado esta función


def obtener_estudiante(id_usuario):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Usuarios WHERE id_usuario = %s ORDER BY id_usuario ASC;", (id_usuario,))
    row = cursor.fetchone()
    conn.close()
    return row


def actualizar_estudiante(
    id_usuario, nombre, apellido, email, contrasena, documento, pais_origen, id_rol
):
    query = """
        UPDATE Usuarios
        SET nombre = %s, apellido = %s, email = %s,
            documento = %s, pais_origen = %s, id_rol = %s
        WHERE id_usuario = %s
    """
    values = [nombre, apellido, email, documento, pais_origen, id_rol, id_usuario]

    if contrasena and contrasena.strip() != "":
        query = """
            UPDATE Usuarios
            SET nombre = %s, apellido = %s, email = %s,
                contrasena = %s, documento = %s, pais_origen = %s, id_rol = %s
            WHERE id_usuario = %s
        """
        hashed = generate_password_hash(contrasena)
        values = [
            nombre,
            apellido,
            email,
            hashed,
            documento,
            pais_origen,
            id_rol,
            id_usuario,
        ]
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(query, values)
    conn.commit()
    conn.close()


def crear_estudiante(nombre, apellido, email, contrasena, documento, pais_origen):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    id_rol = 3  # Por defecto: estudiante
    hashed = generate_password_hash(contrasena)
    cursor.execute(
        "INSERT INTO Usuarios (nombre, apellido, email, contrasena, documento, pais_origen, id_rol) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (nombre, apellido, email, hashed, documento, pais_origen, id_rol),
    )
    conn.commit()
    conn.close()


def crear_estudiantes_bulk(lista_estudiantes):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        id_rol = 3  # Por defecto: estudiante
        for estudiante in lista_estudiantes:
            cursor.execute(
                """
                INSERT INTO Usuarios (nombre, apellido, email, contrasena, documento, pais_origen, id_rol)
                VALUES (%s, %s, %s, %s, %s, %s)
            """,
                (
                    estudiante["nombre"],
                    estudiante["apellido"],
                    estudiante["email"],
                    estudiante["contrasena"],
                    estudiante["documento"],
                    estudiante["pais_origen"],
                    id_rol,
                ),
            )
        conn.commit()
    except Exception as e:
        print("Error al crear estudiantes:", e)
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()


def eliminar_estudiante(id_usuario):
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("DELETE FROM Usuarios WHERE id_usuario = %s", (id_usuario,))
        conn.commit()
        conn.close()
    except psycopg2.Error as e:
        conn.rollback()
        return {"status": "error", "mensaje": "Error al eliminar: " + str(e)}

# ------------------------
# def obtener_materias_estudiante(id_usuario):
#     conn = get_connection()
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
#     # Trae id_inscripcion, id_curso, nombre de curso y nota_final (si existe)
#     cursor.execute("""
#         SELECT i.id_inscripcion,
#                c.id_curso,
#                c.nombre AS nombre_curso,
#                n.nota_final
#         FROM inscripciones i
#         JOIN cursos c USING(id_curso)
#         LEFT JOIN notas n USING(id_inscripcion)
#         WHERE i.id_usuario = %s;
#     """, (id_usuario,))
#     rows = cursor.fetchall()
#     conn.close()
#     return rows


def obtener_materias_estudiante(id_usuario,cursor):
    cursor.execute("""
        SELECT i.id_inscripcion,
               c.id_curso,
               c.nombre AS nombre_curso,
               n.nota_final
        FROM inscripciones i
        JOIN cursos c USING(id_curso)
        LEFT JOIN notas n USING(id_inscripcion)
        WHERE i.id_usuario = %s;
    """, (id_usuario,))
    return cursor.fetchall()

 


# def obtener_cursos_disponibles(id_usuario):
#     conn = get_connection()
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
#     cursor.execute("""
#         SELECT id_curso, nombre
#         FROM cursos
#         WHERE id_curso NOT IN (
#             SELECT id_curso FROM inscripciones WHERE id_usuario = %s
#         )
#         ORDER BY nombre;
#     """, (id_usuario,))
#     rows = cursor.fetchall()
#     conn.close()
#     return rows


def obtener_cursos_disponibles(id_usuario,cursor):
    cursor.execute("""
        SELECT id_curso, nombre
        FROM cursos
        WHERE id_curso NOT IN (
            SELECT id_curso FROM inscripciones WHERE id_usuario = %s
        )
        ORDER BY nombre;
    """, (id_usuario,))
    return cursor.fetchall()
    
def crear_inscripcion(id_usuario, id_curso):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO inscripciones (id_usuario, id_curso, fecha_inscripcion) VALUES (%s, %s, CURRENT_DATE)",
        (id_usuario, id_curso)
    )
    conn.commit()
    conn.close()

def eliminar_inscripcion(id_inscripcion):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inscripciones WHERE id_inscripcion = %s", (id_inscripcion,))
    conn.commit()
    conn.close()


#--------------
# --- Usuarios Expositor


def actualizar_ponente(
    id_usuario, nombre, apellido, email, contrasena, documento, pais_origen, id_rol
):
    query = """
        UPDATE Usuarios
        SET nombre = %s, apellido = %s, email = %s,
            documento = %s, pais_origen = %s, id_rol = %s
        WHERE id_usuario = %s
    """
    values = [nombre, apellido, email, documento, pais_origen, id_rol, id_usuario]

    if contrasena and contrasena.strip() != "":
        query = """
            UPDATE Usuarios
            SET nombre = %s, apellido = %s, email = %s,
                contrasena = %s, documento = %s, pais_origen = %s, id_rol = %s
            WHERE id_usuario = %s
        """
        hashed = generate_password_hash(contrasena)
        values = [
            nombre,
            apellido,
            email,
            hashed,
            documento,
            pais_origen,
            id_rol,
            id_usuario,
        ]
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(query, values)
    conn.commit()
    conn.close()


def crear_ponente(nombre, apellido, email, contrasena, documento, pais_origen):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    id_rol = 2  # Por defecto: ponente
    hashed = generate_password_hash(contrasena)
    cursor.execute(
        "INSERT INTO Usuarios (nombre, apellido, email, contrasena, documento, pais_origen, id_rol) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (nombre, apellido, email, hashed, documento, pais_origen, id_rol),
    )
    conn.commit()
    conn.close()


def crear_ponentes_bulk(lista_expositores):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        id_rol = 2  # Por defecto: ponentes
        for expositor in lista_expositores:
            cursor.execute(
                """
                INSERT INTO Usuarios (nombre, apellido, email, contrasena, documento, pais_origen, id_rol)
                VALUES (%s, %s, %s, %s, %s, %s)
            """,
                (
                    expositor["nombre"],
                    expositor["apellido"],
                    expositor["email"],
                    expositor["contrasena"],
                    expositor["documento"],
                    expositor["pais_origen"],
                    id_rol,
                ),
            )
        conn.commit()
    except Exception as e:
        print("Error al crear ponentes:", e)
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()


def eliminar_ponente(id_usuario):
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("DELETE FROM Usuarios WHERE id_usuario = %s", (id_usuario,))
        conn.commit()
        conn.close()
    except psycopg2.Error as e:
        conn.rollback()
        return {"status": "error", "mensaje": "Error al eliminar: " + str(e)}


# ------------------------

# Cursos dictados por el ponente
def get_cursos_ponente(id_usuario):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.id_curso, c.nombre, c.descripcion
        FROM cursos c
        WHERE c.id_ponente = %s
    """, (id_usuario,))
    cursos = cursor.fetchall()
    result = [{'id_curso': c[0], 'nombre': c[1], 'descripcion': c[2]} for c in cursos]
    cursor.close()
    conn.close()
    return (result)

# Cursos disponibles (sin ponente)
def get_cursos_disponibles_para_ponente():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id_curso, nombre, descripcion
        FROM cursos
        WHERE id_ponente = 1
    """)
    cursos = cursor.fetchall()
    result = [{'id_curso': c[0], 'nombre': c[1], 'descripcion': c[2]} for c in cursos]
    cursor.close()
    conn.close()
    return (result)

# Asignar curso a ponente
def asignar_curso_a_ponente(id_usuario, id_curso):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE cursos SET id_ponente = %s WHERE id_curso = %s
    """, (id_usuario, id_curso))
    conn.commit()
    cursor.close()
    conn.close()

# Quitar curso al ponente
def quitar_curso_a_ponente(id_curso):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE cursos SET id_ponente = 1 WHERE id_curso = %s
    """, (id_curso,))
    conn.commit()
    cursor.close()
    conn.close()

# ------------------------