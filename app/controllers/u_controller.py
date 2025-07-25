import psycopg2
from app.db_c import get_connection
def obtener_estudiantes():
    conn = get_connection() # conecta a la base de datos
    cursor = conn.cursor() # crea un cursor (como el "puente" para hacer consultas)
    cursor.execute("SELECT * FROM Usuarios") # consulta SQL directa
    rows = cursor.fetchall() # obtiene todos los resultados en una lista
    conn.close()  # cierra la conexión
    return rows    # devuelve los datos a quien haya llamado esta función
def obtener_estudiante(id_usuario):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Usuarios WHERE id_usuario = %s", (id_usuario,))
    row = cursor.fetchone()
    conn.close()
    return row


'''def crear_estudiante(nombre, apellido, email, contrasena, documento, pais_origen):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Usuarios (nombre, apellido, email, contrasena, documento, pais_origen) VALUES (%s, %s, %s,%s, %s, %s)", (nombre, apellido, email, contrasena, documento, pais_origen))
    conn.commit()
    conn.close()'''

def crear_estudiante(nombre, apellido, email, contrasena, documento, pais_origen):
    conn = get_connection()
    cursor = conn.cursor()
    #id_rol = 1  # Por defecto: estudiante
    cursor.execute("INSERT INTO Usuarios (nombre, apellido, email, contrasena, documento, pais_origen, id_rol) VALUES (%s, %s, %s, %s, %s, %s, %s)", (nombre, apellido, email, contrasena, documento, pais_origen, id_rol))
    conn.commit()
    conn.close()

'''
def actualizar_estudiante(id_usuario, nombre, apellido, email, contrasena, documento, pais_origen):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Usuarios SET nombre = %s, apellido = %s, email = %s,contrasena = %s,documento = %s,pais_origen = %s WHERE id_usuario = %s",
                   (nombre, apellido, email, contrasena, documento, pais_origen, id_usuario,))
    conn.commit()
    conn.close()'''

def actualizar_estudiante(id_usuario, nombre, apellido, email, contrasena, documento, pais_origen, id_rol):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Usuarios SET nombre = %s, apellido = %s, email = %s, contrasena = %s, documento = %s, pais_origen = %s, id_rol = %s WHERE id_usuario = %s", (nombre, apellido, email, contrasena, documento, pais_origen, id_rol, id_usuario))
    conn.commit()
    conn.close()


def eliminar_estudiante(id_usuario):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Usuarios WHERE id_usuario = %s", (id_usuario,))
        conn.commit()
        conn.close()
    except psycopg2.Error as e:
        conn.rollback()
        return {"status": "error", "mensaje": "Error al eliminar: " + str(e)}
