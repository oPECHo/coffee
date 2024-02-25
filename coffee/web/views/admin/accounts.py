from flask import Blueprint, render_template, redirect, session, url_for
from flask_login import login_user, login_required, logout_user

import datetime

from coffee.web import models, forms, acl

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

module = Blueprint("accounts", __name__, url_prefix="/accounts")


@module.route("/")
@acl.roles_required("admin")
def index():
    accounts = models.User.objects()
    return render_template(
        "admin/accounts/index.html",
        accounts=accounts,
    )


@module.route("/user/<user_id>/setup_password", methods=["GET", "POST"])
def setup_password(user_id):
    user = models.User.objects.get(id=user_id)
    form = forms.accounts.SetupPassword(obj=user)

    if not form.validate_on_submit():
        print(form.errors)
        return render_template("admin/accounts/setup-password.html", form=form)

    # Set the hashed password directly to the user's password field
    user.set_password(form.password.data)
    user.save()

    return redirect(url_for("accounts.login"))
