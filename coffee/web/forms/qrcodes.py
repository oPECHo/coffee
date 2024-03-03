from flask_mongoengine.wtf import model_form
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from coffee import models

BaseBotForm = model_form(
    models.Bot,
    FlaskForm,
    exclude=[
        "created_date",
        "updated_date",
        "document",
    ],
    field_args={
        "document": {"label": "Upload file"},
    },
)


class BotForm(BaseBotForm):
    document_upload = FileField(
        "Upload image QRcode",
        validators=[
            FileAllowed(
                ["png", "jpg", "bmp", "webp", "tiff"], "only JPG, PNG, bmp, webp, tiff"
            )
        ],
    )
