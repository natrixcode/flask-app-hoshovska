from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
    Regexp,
)
from sqlalchemy import select

from app import db
from app.users.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Ім'я користувача",
        validators=[
            DataRequired(),
            Length(min=4, max=14),
            Regexp(
                r"^[A-Za-z0-9._]+$",
                message="Дозволені лише латинські літери, цифри, крапка та _.",
            ),
        ],
    )

    email = StringField(
        "Електронна пошта",
        validators=[
            DataRequired(),
            Email(),
        ],
    )

    password = PasswordField(
        "Пароль",
        validators=[
            DataRequired(),
            Length(min=8, max=72, message="Пароль повинен містити від 8 до 72 символів."),
        ],
    )

    confirm_password = PasswordField(
        "Підтвердження пароля",
        validators=[
            DataRequired(),
            EqualTo("password", message="Паролі не збігаються."),
        ],
    )

    submit = SubmitField("Зареєструватися")

    def validate_username(self, field):
        user = db.session.scalar(
            select(User).where(User.username == field.data)
        )
        if user:
            raise ValidationError("Це ім'я користувача вже зайняте.")

    def validate_email(self, field):
        user = db.session.scalar(
            select(User).where(User.email == field.data)
        )
        if user:
            raise ValidationError("Ця електронна пошта вже зареєстрована.")



class LoginForm(FlaskForm):
    username = StringField(
        "Ім'я користувача",
        validators=[
            DataRequired(message="Введіть ім'я користувача."),
        ],
    )

    password = PasswordField(
        "Пароль",
        validators=[
            DataRequired(message="Введіть пароль."),
        ],
    )

    remember = BooleanField("Запам'ятати мене")

    submit = SubmitField("Увійти")
