from flask import Blueprint, render_template, Response

from coffee.web import models

module = Blueprint("home", __name__, url_prefix="/home")


@module.route("/", methods=["GET", "POST"])
def index():
    qrcodes = models.Bot.objects()
    return render_template(
        "home/index.html",
        qrcodes=qrcodes,
    )

@module.route("/<document_id>/picture/<filename>")
def get_image(document_id, filename):
    response = Response()
    response.status_code = 404

    qrcode = models.Bot.objects(id=document_id).first()
    response = qrcode.get_picture()
    # if note.document:
    #     response = send_file(
    #         note.document,
    #         download_name=note.document.filename,
    #         mimetype=note.document.content_type,
    #     )
    return response