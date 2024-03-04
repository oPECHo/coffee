from flask_wtf import FlaskForm
from wtforms import fields, validators

from flask_mongoengine.wtf import model_form
from coffee import models

Profile = model_form(
    models.User,
    FlaskForm,
    exclude=[
        "created_date",
        "updated_date",
        "last_login_date",
        "email",
        "password",
        "status",
        "first_name",
        "last_name",
        "username",
    ],
    field_args={
    },
)


class UserRolesForm(Profile):
    roles = fields.SelectMultipleField("ตำแหน่ง")