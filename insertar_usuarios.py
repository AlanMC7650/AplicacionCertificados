import psycopg2
from psycopg2 import sql
from werkzeug.security import generate_password_hash

# Datos de conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
    dbname="unesco",
    user="postgres",
    password="13694538Lp",
    host="localhost",
    port="5432",
)


def insertar_usuario(nombre, apellido, email, contrasena_plana, documento, pais_origen, id_rol):
    # Hashear la contraseña usando werkzeug (por defecto usa pbkdf2:sha256)
    contrasena_hashed = generate_password_hash(contrasena_plana)

    with conn.cursor() as cur:
        query = sql.SQL(
            """
            INSERT INTO usuarios (nombre, apellido, email, contrasena, documento, pais_origen, id_rol)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
        )
        cur.execute(
            query,
            (nombre, apellido, email, contrasena_hashed, documento, pais_origen, id_rol),
        )
        conn.commit()
    print("Usuario insertado correctamente.")


# Ejemplo de uso
if __name__ == "__main__":
    insertar_usuario(
        nombre="Michael",
        apellido="Quispe",
        email="mquispel@fcpn.edu.bo",
        contrasena_plana="coordinador",
        documento="coordinador",
        pais_origen="Bolivia",
        id_rol=1
    )
    conn.close()
