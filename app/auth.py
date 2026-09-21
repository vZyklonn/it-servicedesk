from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from app import db
from app.forms import LoginForm, RegisterForm
from app.models import User


auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.strip().lower()

        if User.query.filter_by(username=username).first():
            flash("Dieser Benutzername ist bereits vergeben.", "danger")
            return render_template("register.html", form=form)

        if User.query.filter_by(email=email).first():
            flash("Diese E-Mail-Adresse ist bereits registriert.", "danger")
            return render_template("register.html", form=form)

        user = User(
            username=username,
            email=email
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Registrierung erfolgreich. Du kannst dich jetzt anmelden.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(
            username=form.username.data.strip()
        ).first()

        if user is None or not user.check_password(form.password.data):
            flash("Benutzername oder Passwort ist falsch.", "danger")
            return render_template("login.html", form=form)

        login_user(user)

        return redirect(url_for("main.dashboard"))

    return render_template("login.html", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))
