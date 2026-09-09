from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)

from db import db_session
from auth.forms import EditProfileForm, LoginForm, RegisterForm
from models import User

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db_session.add(user)
        db_session.commit()
        flash("Регистрация успешна", "success")
        return redirect(url_for("items.home"))
    return render_template("register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_session.query(User).filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Вы вошли", "success")
            return redirect(url_for("items.home"))
        return "Неверный логин и пароль", 401
    return render_template("login.html", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    flash("Вы вышли", "info")
    return redirect(url_for("items.home"))


@bp.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@bp.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.password.data:
            current_user.set_password(form.password.data)
        db_session.commit()
        flash("Профиль обновлён", "success")
        return redirect(url_for("auth.profile"))
    return render_template("edit_profile.html", form=form)
