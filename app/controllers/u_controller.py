import psycopg2
from app.db_c import get_connection
from werkzeug.security import generate_password_hash
# --- Usuarios General
def obtener_usuarios(rol):
    conn = get_connection()  # conecta a la base de datos
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM Usuarios WHERE id_rol = %s ORDER BY id_usuario ASC;",(rol,))  # consulta SQL directa
    rows = cursor.fetchall()  # obtiene todos los resultados en una lista
    conn.close()  # cierra la conexión
    return rows  # devuelve los datos a quien haya llamado esta función

def obtener_usuarios_id(rol,id):
    conn = get_connection()  # conecta a la base de datos
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM Usuarios WHERE id_rol = %s and id_usuario=%s",(rol,id))  # consulta SQL directa
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
        values = [nombre, apellido, email, hashed, documento, pais_origen, id_rol, id_usuario]
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
                    id_rol
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
        values = [nombre, apellido, email, hashed, documento, pais_origen, id_rol, id_usuario]
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
                    id_rol
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
