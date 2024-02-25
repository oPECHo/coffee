from flask_mongoengine.wtf import model_form
from flask_wtf import FlaskForm, file
from wtforms import fields, widgets, validators
import email_validator

import datetime

from coffee import models

BaseRegistrationForm = model_form(
    models.User,
    FlaskForm,
    exclude=[
        "created_date",
        "updated_date",
        "roles",
        "last_login_date",
        "status",
    ],
    field_args={
        "username": {"label": "Username"},
        "first_name": {"label": "Firstname"},
        "last_name": {"label": "Lastname"},
    },
)


class RegistrationForm(BaseRegistrationForm):
    password = fields.PasswordField(
        "Password", validators=[validators.InputRequired(), validators.Length(min=6)]
    )
    email = fields.StringField(
        "Email", validators=[validators.Email(), validators.DataRequired()]
    )


class LoginForm(FlaskForm):
    username = fields.StringField("Username", validators=[validators.DataRequired()])
    password = fields.PasswordField("password", validators=[validators.InputRequired()])
    submit = fields.SubmitField("Login")

class SetupPassword(FlaskForm):
    password = fields.PasswordField(
        "New Password", validators=[validators.DataRequired()]
    )
    confirm_password = fields.PasswordField(
        "Confirm Password",
        validators=[
            validators.InputRequired(),
            validators.Length(min=6),
            validators.EqualTo("password", message="รหัสผ่านไม่ตรงกัน"),
        ],
    )