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
