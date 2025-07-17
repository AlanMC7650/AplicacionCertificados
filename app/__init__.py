from flask import Flask
from dotenv import load_dotenv
from .extensions import db, mail
from datetime import timedelta
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
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)

    db.init_app(app)
    mail.init_app(app)

    # Añadimos el blueprint a nuestra aplicación
    from app.api.auth import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/")

    with app.app_context():
        db.create_all()

    return app
