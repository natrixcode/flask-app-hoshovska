from flask import Blueprint, render_template, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, current_user, login_required, logout_user

from app import db
from app.users.models import User
from app.users.forms import RegistrationForm, LoginForm

users_bp = Blueprint("users", __name__, template_folder="templates")


@users_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Користувач із такими даними вже існує.", "danger")
        else:
            flash("Реєстрація успішна! Тепер можна увійти.", "success")
            return redirect(url_for("users.register"))

    return render_template("users/register.html", form=form)



@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("users.account"))

    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.scalar(
            db.select(User).where(User.username == form.username.data)
        )

        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Ви успішно увійшли в систему!", "success")
            return redirect(url_for("users.account"))

        flash("Неправильне ім'я користувача або пароль.", "danger")

    return render_template("users/login.html", form=form)



@users_bp.route("/account")
@login_required
def account():
    return render_template("users/account.html")



@users_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("Ви успішно вийшли із системи.", "success")
    return redirect(url_for("users.login"))



@users_bp.route("/users")
@login_required
def users_list():
    users = db.session.scalars(
        db.select(User).order_by(User.id)
    ).all()

    return render_template(
        "users/list.html",
        users=users,
        total=len(users),
    )
