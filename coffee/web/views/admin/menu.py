from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    Response,
    send_file,
    request,
)
from flask_login import login_required, current_user


import datetime

from coffee.web import models, forms, acl

module = Blueprint("menus", __name__, url_prefix="/menus")


@module.route("/")
@login_required
@acl.roles_required("admin")
def index():
    menus = models.Menu.objects()

    return render_template(
        "admin/menus/index.html",
        menus=menus,
    )


@module.route("/create", methods=["GET", "POST"])
@login_required
@acl.roles_required("admin")
def menus_create():
    form = forms.coffee.MenuForm()
    menu = models.Menu()

    if not form.validate_on_submit():
        print(form.errors)
        return render_template(
            "admin/menus/menu-create-edit.html",
            form=form,
        )

    form.populate_obj(menu)

    if form.document_upload.data:
        print("img_data", form.document_upload.data)
        if not menu.document:
            menu.document.put(
                form.document_upload.data,
                filename=form.document_upload.data.filename,
                content_type=form.document_upload.data.content_type,
            )
        else:
            menu.document.replace(
                form.document_upload.data,
                filename=form.document_upload.data.filename,
                content_type=form.document_upload.data.content_type,
            )

    menu.save()

    return redirect(url_for("admin.menus.index"))


@module.route("/<menu_id>/delete", methods=["GET", "POST"])
@login_required
@acl.roles_required("admin")
def delete(menu_id):
    menu = models.Menu.objects.get(id=menu_id)

    menu.delete()

    return redirect(url_for("admin.menus.index"))


@module.route("/<menu_id>/edit", methods=["GET", "POST"])
@login_required
@acl.roles_required("admin")
def menus_edit(menu_id):
    menu = models.Menu.objects.get(id=menu_id)
    form = forms.coffee.MenuForm(obj=menu)
    if not form.validate_on_submit():
        return render_template(
            "admin/menus/menu-create-edit.html",
            form=form,
            menu=menu,
        )

    form.populate_obj(menu)
    if form.document_upload.data:
        print("img_data", form.document_upload.data)
        if not menu.document:
            menu.document.put(
                form.document_upload.data,
                filename=form.document_upload.data.filename,
                content_type=form.document_upload.data.content_type,
            )
        else:
            menu.document.replace(
                form.document_upload.data,
                filename=form.document_upload.data.filename,
                content_type=form.document_upload.data.content_type,
            )

    menu.updated_date = datetime.datetime.now()
    menu.save()

    return redirect(url_for("admin.menus.index"))
