from flask import Blueprint, render_template, redirect, url_for, Response, send_file
from flask_login import login_required

import datetime

from coffee.web import models, forms, acl

module = Blueprint("menus", __name__, url_prefix="/menus")


@module.route("/")
@login_required
def index():
    menus = models.Menu.objects()
    return render_template(
        "menus/index.html",
        menus=menus,
    )


@module.route("/<document_id>/picture/<filename>")
@login_required
def get_image(document_id, filename):
    response = Response()
    response.status_code = 404

    menu = models.Menu.objects(id=document_id).first()
    response = menu.get_picture()
    # if note.document:
    #     response = send_file(
    #         note.document,
    #         download_name=note.document.filename,
    #         mimetype=note.document.content_type,
    #     )
    return response
