from flask import redirect, url_for, request
from flask_login import current_user, LoginManager, login_url
from werkzeug.exceptions import Forbidden, Unauthorized
from . import models

from functools import wraps

login_manager = LoginManager()


def init_acl(app):
    login_manager.init_app(app)

    @app.errorhandler(401)
    def unauthorized(e):
        return Unauthorized()

    @app.errorhandler(403)
    def forbidden(e):
        return "You don't have permission."


def roles_required(*roles):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                raise Forbidden()

            for role in roles:
                if role in current_user.roles:
                    return func(*args, **kwargs)
            raise Forbidden()

        return wrapped

    return wrapper


@login_manager.user_loader
def load_user(user_id):
    print("user_id", user_id, type(user_id))
    if not user_id or user_id == "None":
        return

    user = models.User.objects(id=user_id, status="active").first()
    return user


@login_manager.unauthorized_handler
def unauthorized_callback():
    print("unauthorized!!\n")
    if request.method == "GET":
        response = redirect(login_url("accounts.login"))
        return response

    return redirect(url_for("accounts.login"))
