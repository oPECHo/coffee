from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    Response,
)
from flask_login import login_required


import datetime

from coffee.web import models, forms, acl

module = Blueprint("qrcodes", __name__, url_prefix="/qrcodes")


@module.route("/")
@login_required
@acl.roles_required("admin")
def index():
    qrcodes = models.Bot.objects()

    return render_template(
        "admin/qrcodes/index.html",
        qrcodes=qrcodes,
    )

@module.route("/<document_id>/picture/<filename>")
@login_required
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

@module.route("/create", methods=["GET", "POST"])
@login_required
@acl.roles_required("admin")
def qrcode_create():
    form = forms.qrcodes.BotForm()
    qrcode = models.Bot()

    if not form.validate_on_submit():
        print(form.errors)
        return render_template(
            "admin/qrcodes/qrcode-create-edit.html",
            form=form,
        )

    form.populate_obj(qrcode)

    if form.document_upload.data:
        print("img_data", form.document_upload.data)
        if not qrcode.document:
            qrcode.document.put(
                form.document_upload.data,
                filename=form.document_upload.data.filename,
                content_type=form.document_upload.data.content_type,
            )
        else:
            qrcode.document.replace(
                form.document_upload.data,
                filename=form.document_upload.data.filename,
                content_type=form.document_upload.data.content_type,
            )

    qrcode.save()

    return redirect(url_for("admin.qrcodes.index"))


@module.route("/<qrcode_id>/delete", methods=["GET", "POST"])
@login_required
@acl.roles_required("admin")
def delete(qrcode_id):
    qrcode = models.Bot.objects.get(id=qrcode_id)

    qrcode.delete()

    return redirect(url_for("admin.qrcodes.index"))


@module.route("/<qrcode_id>/edit", methods=["GET", "POST"])
@login_required
@acl.roles_required("admin")
def qrcode_edit(qrcode_id):
    qrcode = models.Bot.objects.get(id=qrcode_id)
    form = forms.qrcodes.BotForm(obj=qrcode)
    if not form.validate_on_submit():
        return render_template(
            "admin/qrcodes/qrcode-create-edit.html",
            form=form,
            qrcode=qrcode,
        )

    form.populate_obj(qrcode)
    if form.document_upload.data:
        print("img_data", form.document_upload.data)
        if not qrcode.document:
            qrcode.document.put(
                form.document_upload.data,
                filename=form.document_upload.data.filename,
                content_type=form.document_upload.data.content_type,
            )
        else:
            qrcode.document.replace(
                form.document_upload.data,
                filename=form.document_upload.data.filename,
                content_type=form.document_upload.data.content_type,
            )

    qrcode.updated_date = datetime.datetime.now()
    qrcode.save()

    return redirect(url_for("admin.qrcodes.index"))
