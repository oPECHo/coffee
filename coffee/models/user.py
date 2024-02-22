import mongoengine as me
import datetime
from flask_login import UserMixin


class User(me.Document, UserMixin):
    meta = {"collection": "users"}
    username = me.StringField(required=True, unique=True, max_length=64)
    password = me.StringField(required=True)
    first_name = me.StringField(required=True, max_length=128)
    last_name = me.StringField(required=True, max_length=128)
    email = me.StringField(required=True, unique=True)
    roles = me.ListField(me.StringField(), default=["user"])

    created_date = me.DateTimeField(required=True, default=datetime.datetime.now)
    updated_date = me.DateTimeField(required=True, default=datetime.datetime.now)
    last_login_date = me.DateTimeField(
        required=True, default=datetime.datetime.now, auto_now=True
    )
    status = me.StringField(required=True, default="active")
    # update_info = me.EmbeddedDocumentListField("UpdateInformation")

    def set_password(self, password):
        from werkzeug.security import generate_password_hash

        self.password = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash

        if check_password_hash(self.password, password):
            return True
        return False

    def check_roles(self, roles: list):
        if set(roles) & set(self.roles):
            return True
        return False

    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"

    def has_roles(self, *roles):
        for role in roles:
            if role in self.roles:
                return True
        return
