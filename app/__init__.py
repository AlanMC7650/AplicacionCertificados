from flask import Flask
from dotenv import load_dotenv
from .extensions import db, mail
from datetime import timedelta
from flask_login import LoginManager
from app.models.user import Usuario
import os


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["REMEMBER_COOKIE_DURATION"] = timedelta(minutes=1)

    db.init_app(app)
    mail.init_app(app)

    # Añadimos el blueprint auth login a nuestra aplicación
    from app.api.auth import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    # Añadimos el blueprint de qrs a nuestra aplicacion
    from app.api.qrs import qrs_bp

    app.register_blueprint(qrs_bp, url_prefix="/qr")

    # Configuramos Flask Login para manejar sesiones de usuario
    login_manager = LoginManager(app)
    login_manager.login_view = "auth.login"

    # Esto es importante para que Flask_login pueda trabajar
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # Hacer accesible los QRs generados
    with app.app_context():
        db.create_all()

    return app
