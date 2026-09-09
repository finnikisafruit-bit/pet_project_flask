from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import PasswordField, StringField, SubmitField, EmailField
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    ValidationError,
    Optional,
)

from db import db_session
from models import User


class LoginForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password2 = PasswordField(
        "Повторите пароль",
        validators=[DataRequired(), EqualTo("password", message="Пароли не совпадают")],
    )
    submit = SubmitField("Зарегистрироваться")

    def validate_username(self, username):
        if db_session.query(User).filter_by(username=username.data).first():
            raise ValidationError("Пользователь уже существует")

    def validate_email(self, email):
        if db_session.query(User).filter_by(email=email.data).first():
            raise ValidationError("Email уже занят")


class EditProfileForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[Optional()])
    password2 = PasswordField(
        "Повторите пароль",
        validators=[Optional(), EqualTo("password", message="Пароли не совпадают")],
    )
    submit = SubmitField("Сохранить")

    def validate_username(self, username):
        user = db_session.query(User).filter_by(username=username.data).first()
        if user and user.id != current_user.id:
            raise ValidationError("Пользователь уже существует")

    def validate_email(self, email):
        user = db_session.query(User).filter_by(email=email.data).first()
        if user and user.id != current_user.id:
            raise ValidationError("Email уже занят")
