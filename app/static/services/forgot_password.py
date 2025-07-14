from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from werkzeug.security import generate_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import os
from dotenv import load_dotenv

# Carga el archivo .env.example
load_dotenv(dotenv_path='../../../.env')


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'mquispel@fcpn.edu.bo'
app.config['MAIL_PASSWORD'] = 'whfl jxtm enio wnvm'

db = SQLAlchemy(app)
mail = Mail(app)

class User(db.Model):
    __tablename__  = 'usuarios'
    id = db.Column('id_usuario', db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hashed_password = db.Column('contrasena', db.String(200), nullable=False)

class ForgotPasswordForm(FlaskForm):
    email = StringField("Enter your email", validators=[DataRequired(), Email()])
    submit = SubmitField("Send reset link")

class ResetPasswordForm(FlaskForm):
    password = StringField("New Password", validators=[DataRequired()])
    submit = SubmitField("Reset")

def get_reset_token(user_email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(user_email, salt='password-reset-salt')

def send_reset_email(user):
    token = get_reset_token(user.email)
    reset_url = url_for('reset_token', token=token, _external=True)

    msg = Message("Password Reset Request",
                  sender="noreply@yourapp.com",
                  recipients=[user.email])
    msg.body = f"Reset your password: {reset_url}"
    mail.send(msg)
    print(f"[DEBUG] Enviaríamos este link a {user.email}: {reset_url}")


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
        flash("If your email is in our system, you will receive a reset link.", "info")
        return redirect(url_for('forgot_password'))
    return render_template('forgot_password.html', form=form)

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
    except (SignatureExpired, BadSignature):
        flash("That link is invalid or has expired.", "danger")
        return redirect(url_for('forgot_password'))

    user = User.query.filter_by(email=email).first_or_404()
    form = ResetPasswordForm()

    if form.validate_on_submit():
        hashed = generate_password_hash(form.password.data)
        user.hashed_password = hashed
        db.session.commit()
        flash("Your password has been updated!", "success")
        return redirect(url_for('forgot_password'))

    return render_template('reset_password.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)