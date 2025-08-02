import psycopg2
from app.db_c import get_connection


def obtener_cursos_full():
    conn = get_connection()  # conecta a la base de datos
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)  # crea un cursor (como el "puente" para hacer consultas)
    cursor.execute("""SELECT c.*,v.*,u.nombre as NombreU, u.apellido as ApellidoU 
        FROM cursos c JOIN usuarios u ON c.id_ponente = u.id_usuario
        JOIN version_evento v ON c.id_version = v.id_version
        """)  # consulta SQL directa
    rows = cursor.fetchall()  # obtiene todos los resultados en una lista
    conn.close()  # cierra la conexión
    return rows  # devuelve los datos a quien haya llamado esta función

def obtener_cursos():
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM cursos")
                return cursor.fetchall()
    except psycopg2.Error as e:
        print(f"[ERROR] obtener_cursos: {e}")
        return []

def obtener_curso(id_curso):
    try:
        print(f"🔍 Buscando curso con id {id_curso}")
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cursos WHERE id_curso = %s", (id_curso,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row
    except psycopg2.Error as e:
        print(f"[ERROR] obtener_curso: {e}")
        return None


def crear_curso(nombre, descripcion, modalidad, id_version, id_ponente):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO cursos (nombre, descripcion, modalidad, id_version, id_ponente)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (nombre, descripcion, modalidad, id_version, id_ponente),
                )
                conn.commit()
    except psycopg2.Error as e:
        print(f"[ERROR] crear_curso: {e}")

def actualizar_curso(id_curso, nombre, descripcion, modalidad, id_version, id_ponente):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE cursos
                    SET nombre = %s, descripcion = %s, modalidad = %s, id_version = %s, id_ponente = %s
                    WHERE id_curso = %s
                    """,
                    (nombre, descripcion, modalidad, id_version, id_ponente, id_curso),
                )
                conn.commit()
    except psycopg2.Error as e:
        print(f"[ERROR] actualizar_curso: {e}")

def eliminar_curso(id_curso):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM cursos WHERE id_curso = %s", (id_curso,))
                conn.commit()
    except psycopg2.Error as e:
        print(f"[ERROR] eliminar_curso: {e}")
        return {"status": "error", "mensaje": "Error al eliminar: " + str(e)}
