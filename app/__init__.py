# app/__init__.py
from flask import Flask
from dotenv import load_dotenv
from .extensions import db, mail
import os


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = "mquispel@fcpn.edu.bo"
    app.config["MAIL_PASSWORD"] = "whfl jxtm enio wnvm"

    db.init_app(app)
    mail.init_app(app)

    with app.app_context():
        db.create_all()

    from .routes import main_routes

    app.register_blueprint(main_routes)

    return app
