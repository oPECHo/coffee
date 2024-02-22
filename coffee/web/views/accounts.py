from flask import Blueprint, render_template, redirect, session, url_for
from flask_login import login_user, login_required, logout_user

import datetime

from coffee import models
from coffee.web import forms

module = Blueprint("accounts", __name__)


@module.route("/")
def index():
    return render_template("accounts/login.html")


@module.route("/register", methods=["GET", "POST"])
def register():
    form = forms.accounts.RegistrationForm()
    user = models.User()

    if not form.validate_on_submit():
        return render_template("accounts/register.html", form=form)

    form.populate_obj(user)
    user.set_password(form.password.data)
    user.save()

    return redirect(url_for("accounts.login"))


@module.route("/login", methods=["GET", "POST"])
def login():
    form = forms.accounts.LoginForm()

    if form.validate_on_submit():
        user = models.User.objects(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            user.last_login_date = datetime.datetime.now()
            user.save()

            return redirect(url_for("menus.index"))

    return render_template("accounts/login.html", form=form)


@module.route("/logout")
@login_required
def logout():
    # print("logout")
    logout_user()
    session.clear()
    # print("0>", session)

    return redirect(url_for("accounts.login"))
