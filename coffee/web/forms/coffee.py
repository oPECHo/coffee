from flask_mongoengine.wtf import model_form
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from coffee import models

BaseMenuForm = model_form(
    models.Menu,
    FlaskForm,
    exclude=[
        "created_date",
        "updated_date",
        "document",
    ],
    field_args={
        "title": {"label": "Title"},
        "description": {"label": "Description"},
        "priceS": {"label": "PriceS"},
        "priceM": {"label": "PriceM"},
        "priceL": {"label": "PriceL"},
        "document": {"label": "Upload file"},
    },
)


class MenuForm(BaseMenuForm):
    document_upload = FileField(
        "Upload image รูปข่าวสาร",
        validators=[
            FileAllowed(
                ["png", "jpg", "bmp", "webp", "tiff"], "only JPG, PNG, bmp, webp, tiff"
            )
        ],
    )
