from flask import Blueprint, render_template

module = Blueprint("home", __name__, url_prefix="/home")


@module.route("/", methods=["GET", "POST"])
def index():
    return render_template(
        "home/index.html",
    )
