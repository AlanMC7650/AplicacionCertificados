import os
from flask import (
    Flask,
    render_template,
)  # //render_template para mostrar archivos HTML desde la carpeta templates.
from app.static.services.forgot_password import forgot_password
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(
        BASE_DIR, "templates"
    ),  # //indicamos donde se encuentras las carpetas
    static_folder=os.path.join(
        BASE_DIR, "static"
    ),  # //todo esto solo sirve para estructuras no estandares, osea para esta vista sirve bien pero para el proyecto en general no sirve
)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password_route():
    return forgot_password()


@app.route("/")
def login():
    return render_template("login.html")  # //para mostrar la vista del html


@app.route("/dashboard")
def dashboard():
    return render_template(
        "dashboard.html", nombre="DIEGO ANDRÉS FLORES GUTIERREZ"
    )  # // ya que no hay base de datos aqui insertamos el nombre del estudiante a mostrar en la vista de dashboard


if __name__ == "__main__":
    app.run(debug=True)
