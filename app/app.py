# app.py
from app import create_app  # importa tu fábrica de aplicación

app = create_app()  # inicializa correctamente tu aplicación

# Ya no necesitas definir rutas aquí si usas blueprints

if __name__ == "__main__":
    app.run(debug=True)
